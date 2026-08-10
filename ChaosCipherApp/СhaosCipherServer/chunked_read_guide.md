# HTTP + Chunked Read: реалізація на бекенді ChaosCipherServer

## Поточна проблема

Усі ендпоінти зараз читають файл **цілком у RAM** одним викликом:

```python
# main.py — кожен ендпоінт робить так:
original_file = await file.read()  # ← весь файл одразу в пам'ять
```

Для файлу 200 MB це означає **~200 MB RAM** лише на читання, плюс ще стільки ж на генерацію ключа і результат шифрування. Підсумкове споживання: **~600 MB на один запит**.

---

## Рішення: поблочне читання (`chunked read`)

Замість `await file.read()` читаємо файл порціями по 64 KB. Це **не змінює логіку шифрування** — просто зменшує пік пам'яті на етапі зчитування.

> [!IMPORTANT]
> Це **не** стрімове шифрування (яке вже є закоментованим у коді). Це простіший підхід: читаємо файл чанками, збираємо в `bytes`, передаємо в існуючі функції шифрування **без змін**.

---

## Зміни по файлах

### 1. [main.py](file:///c:/Users/sasha/Desktop/%D0%94%D0%B8%D0%BF%D0%BB%D0%BE%D0%BC%2025/ChaosCipher/ChaosCipherApp/%D0%A1haosCipherServer/main.py) — ендпоінти

#### Допоміжна функція (додати на початку файлу після імпортів)

```python
async def read_upload_chunked(file: UploadFile, chunk_size: int = 64 * 1024) -> bytes:
    """Читає UploadFile порціями, щоб не тримати весь буфер у пам'яті uvicorn."""
    chunks = []
    while chunk := await file.read(chunk_size):
        chunks.append(chunk)
    return b"".join(chunks)
```

#### Замінити `await file.read()` → `await read_upload_chunked(file)`

Зміни однакові для всіх файлових ендпоінтів:

```diff
 @app.post("/encrypt/file")
 async def encrypt_file_enpoint(...):
     try:
-        original_file = await file.read()
+        original_file = await read_upload_chunked(file)
         params_obj = json.loads(params)
```

Повний список ендпоінтів, де потрібна заміна (6 місць):

| Ендпоінт | Рядок у main.py |
|---|---|
| `POST /encrypt/image` | рядок 43 |
| `POST /decrypt/image` | рядок 77 |
| `POST /encrypt/audio` | рядок 173 |
| `POST /decrypt/audio` | рядок 206 |
| `POST /encrypt/file` | рядок 237 |
| `POST /decrypt/file` | рядок 277 |

> [!NOTE]
> Текстові ендпоінти (`/encrypt/text`, `/decrypt/text`) передають `text: str = Form(...)`, а не файл — їх змінювати **не потрібно**.

---

### 2. Запуск uvicorn — збільшити ліміт розміру запиту

За замовчуванням uvicorn обмежує тіло запиту розміром **1 MB**. Для великих файлів потрібно збільшити:

```bash
# Варіант 1: через CLI (рекомендовано)
uvicorn main:app --host 0.0.0.0 --port 8000 --limit-max-request-size 209715200
#                                              ↑ 200 MB у байтах

# Варіант 2: програмно в main.py
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        limit_max_request_size=200 * 1024 * 1024,  # 200 MB
    )
```

---

### 3. Оновити ліміти в модулях шифрування

Поточні ліміти в модулях шифрування:

| Файл | Константа | Поточне значення |
|---|---|---|
| [file_encrypt.py](file:///c:/Users/sasha/Desktop/%D0%94%D0%B8%D0%BF%D0%BB%D0%BE%D0%BC%2025/ChaosCipher/ChaosCipherApp/%D0%A1haosCipherServer/encrypt_alg/file_encrypt.py) | `MAX_FILE_SIZE` | 100 MB |
| [audio_encrypt.py](file:///c:/Users/sasha/Desktop/%D0%94%D0%B8%D0%BF%D0%BB%D0%BE%D0%BC%2025/ChaosCipher/ChaosCipherApp/%D0%A1haosCipherServer/encrypt_alg/audio_encrypt.py) | `MAX_AUDIO_SIZE` | 1000 MB |

Якщо бажаний максимум — 200 MB, встановити однаковий ліміт:

```diff
 # file_encrypt.py
-MAX_FILE_SIZE = 100 * 1024 * 1024
+MAX_FILE_SIZE = 200 * 1024 * 1024  # 200 МБ

 # audio_encrypt.py
-MAX_AUDIO_SIZE = 1000 * 1024 * 1024
+MAX_AUDIO_SIZE = 200 * 1024 * 1024  # 200 МБ
```

---

## Чому цього достатньо

XOR-шифрування, яке використовується в проекті, **вже працює з повним масивом байтів**. Функції `encrypt_file`, `encrypt_auido`, `encrypt_image` приймають `bytes` — chunked read просто змінює спосіб **зчитування** цих байтів із мережевого потоку, не торкаючись логіки шифрування.

```
Було:   [Мережа] ---(весь файл одразу)---> [RAM] ---> encrypt()
Стало:  [Мережа] ---(64KB, 64KB, ...)---> [RAM] ---> encrypt()
```

Пік RAM все одно буде приблизно рівний розміру файлу (бо шифрування batch), але **зчитування** не створить додаткового пікового навантаження від буферів uvicorn.

---

## Підсумок змін

| Що змінити | Де | Скільки рядків |
|---|---|---|
| Додати `read_upload_chunked()` | `main.py`, після імпортів | +4 рядки |
| Замінити `await file.read()` | `main.py`, 6 ендпоінтів | 6 × 1 рядок |
| Збільшити ліміт uvicorn | CLI або `main.py` | +1 рядок |
| Вирівняти `MAX_*_SIZE` | `file_encrypt.py`, `audio_encrypt.py` | 2 × 1 рядок |

**Загалом: ~12 рядків змін, 0 змін в логіці шифрування.**
