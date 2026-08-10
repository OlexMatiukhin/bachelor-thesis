"""
Загальні фікстури для тестів ChaosCipherServer.
"""
import sys
import pytest
import numpy as np
from pathlib import Path
from io import BytesIO

# Додаємо кореневу директорію проєкту в sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# ─── Параметри для кожної хаотичної системи ───────────────────────────
LORENZ_PARAMS = {"logisticXLorenz": 0.1, "lorenzX": 0, "lorenzY": 0, "lorenzZ": 0}
ROSSLER_PARAMS = {"logisticXRossler": 0.3, "rosslerX": 1.0, "rosslerY": 1.0, "rosslerZ": 1.0}
CHUA_PARAMS = {"logisticXChua": 0.3, "chuaX": 0.1, "chuaY": 0.0, "chuaZ": 0.0}
DUFFING_PARAMS = {"logisticXDuffing": 0.3, "duffingX": 0.1, "duffingY": 0.0, "duffingT": 0.0}
VAN_DER_POL_PARAMS = {"logisticXPol": 0.3, "polX": 0.1, "polY": 0.0, "polT": 0.0}
FORCED_PARAMS = {"logisticXForced": 0.3, "forcedX": 0.1, "forcedY": 0.0, "forcedT": 0.0}

ALL_SYSTEM_CONFIGS = [
    ("lorenz", LORENZ_PARAMS),
    ("rossler", ROSSLER_PARAMS),
    ("chua", CHUA_PARAMS),
    ("duffing", DUFFING_PARAMS),
    ("pol", VAN_DER_POL_PARAMS),
    ("forced", FORCED_PARAMS),
]

# ─── Фікстури ─────────────────────────────────────────────────────────

@pytest.fixture
def chaos_factory():
    from generators import ChaosFactory
    return ChaosFactory()


@pytest.fixture(params=ALL_SYSTEM_CONFIGS, ids=[c[0] for c in ALL_SYSTEM_CONFIGS])
def system_config(request):
    """Повертає (system_type, params) для параметризованих тестів по всіх системах."""
    return request.param


@pytest.fixture
def make_generator(chaos_factory):
    """Фабрика для створення генераторів з заданими параметрами."""
    def _make(system_type, params, mode="chars"):
        return chaos_factory.create_generator(system_type, params, mode)
    return _make


@pytest.fixture
def lorenz_generator_chars(make_generator):
    return make_generator("lorenz", LORENZ_PARAMS, "chars")


@pytest.fixture
def lorenz_generator_bytes(make_generator):
    return make_generator("lorenz", LORENZ_PARAMS, "bytes")


@pytest.fixture
def test_image_bytes():
    """Створює тестове PNG-зображення 3×5 (не квадратне, щоб спрацював header embedding)."""
    import PIL.Image as Image
    pixels = np.array([
        [[255, 0, 0], [0, 255, 0], [0, 0, 255], [128, 128, 0], [0, 128, 128]],
        [[64, 64, 64], [192, 192, 192], [255, 255, 0], [0, 255, 255], [255, 0, 255]],
        [[10, 20, 30], [40, 50, 60], [70, 80, 90], [100, 110, 120], [130, 140, 150]],
    ], dtype=np.uint8)
    img = Image.fromarray(pixels, "RGB")
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


@pytest.fixture
def test_wav_bytes():
    """Створює мінімальний WAV-файл (44100 Hz, 16-bit, 50ms sine 440 Hz)."""
    import soundfile as sf
    sr = 44100
    duration = 0.05
    samples = int(sr * duration)
    t = np.linspace(0, duration, samples, endpoint=False)
    data = (np.sin(2 * np.pi * 440 * t) * 32767).astype(np.int16)
    buf = BytesIO()
    sf.write(buf, data, sr, format="WAV", subtype="PCM_16")
    return buf.getvalue()
