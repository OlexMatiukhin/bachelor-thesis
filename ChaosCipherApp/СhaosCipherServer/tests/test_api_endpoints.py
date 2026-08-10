"""
Рівень 6 — Тести API-ендпоінтів (main.py).
Використовуємо FastAPI TestClient.
"""
import json
import pytest
from fastapi.testclient import TestClient
from conftest import LORENZ_PARAMS


@pytest.fixture
def client():
    from main import app
    return TestClient(app)


LORENZ_PARAMS_JSON = json.dumps(LORENZ_PARAMS)


class TestTextEndpoints:

    def test_encrypt_text(self, client):
        response = client.post("/encrypt/text", data={
            "system": "lorenz",
            "params": LORENZ_PARAMS_JSON,
            "data_type": "text",
            "mode": "chars",
            "text": "Hello, World!",
        })
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "processed_text" in data

    def test_encrypt_decrypt_text_roundtrip(self, client):
        original = "Тестовий текст API"
        enc_resp = client.post("/encrypt/text", data={
            "system": "lorenz",
            "params": LORENZ_PARAMS_JSON,
            "data_type": "text",
            "mode": "chars",
            "text": original,
        })
        assert enc_resp.status_code == 200
        encrypted = enc_resp.json()["processed_text"]

        dec_resp = client.post("/decrypt/text", data={
            "system": "lorenz",
            "params": LORENZ_PARAMS_JSON,
            "data_type": "text",
            "mode": "chars",
            "text": encrypted,
        })
        assert dec_resp.status_code == 200
        assert dec_resp.json()["processed_text"] == original


class TestImageEndpoints:

    def test_encrypt_image(self, client, test_image_bytes):
        response = client.post("/encrypt/image", data={
            "system": "lorenz",
            "params": LORENZ_PARAMS_JSON,
            "data_type": "image",
            "mode": "chars",
        }, files={"file": ("test.png", test_image_bytes, "image/png")})
        assert response.status_code == 200
        assert response.headers["content-type"] == "image/png"

    def test_decrypt_unencrypted_image_throws_error(self, client, test_image_bytes):

        dec_resp = client.post("/decrypt/image", data={
            "system": "lorenz",
            "params": LORENZ_PARAMS_JSON,
            "data_type": "image",
            "mode": "chars",
        }, files={"file": ("encrypted.png", test_image_bytes, "image/png")})
        assert dec_resp.status_code == 400

    def test_encrypt_decrypt_image_roundtrip(self, client, test_image_bytes):
            enc_resp = client.post("/encrypt/image", data={
                "system": "lorenz",
                "params": LORENZ_PARAMS_JSON,
                "data_type": "image",
                "mode": "chars",
            }, files={"file": ("test.png", test_image_bytes, "image/png")})
            assert enc_resp.status_code == 200

            dec_resp = client.post("/decrypt/image", data={
                "system": "lorenz",
                "params": LORENZ_PARAMS_JSON,
                "data_type": "image",
                "mode": "chars",
            }, files={"file": ("encrypted.png", enc_resp.content, "image/png")})
            assert dec_resp.status_code == 200


class TestAudioEndpoints:

    def test_encrypt_audio(self, client, test_wav_bytes):
        response = client.post("/encrypt/audio", data={
            "system": "lorenz",
            "params": LORENZ_PARAMS_JSON,
            "data_type": "audio",
        }, files={"file": ("test.wav", test_wav_bytes, "audio/wav")})
        assert response.status_code == 200


class TestFileEndpoints:

    def test_encrypt_file(self, client):
        response = client.post("/encrypt/file", data={
            "system": "lorenz",
            "params": LORENZ_PARAMS_JSON,
            "data_type": "file",
        }, files={"file": ("test.bin", b"binary data here", "application/octet-stream")})
        assert response.status_code == 200
        assert "processed" in response.headers.get("content-disposition", "")


class TestErrorHandling:

    def test_unknown_system(self, client):
        response = client.post("/encrypt/text", data={
            "system": "unknown_system",
            "params": LORENZ_PARAMS_JSON,
            "data_type": "text",
            "mode": "chars",
            "text": "test",
        })
        assert response.status_code in (400, 500)

    def test_invalid_json_params(self, client):
        response = client.post("/encrypt/text", data={
            "system": "lorenz",
            "params": "not valid json",
            "data_type": "text",
            "mode": "chars",
            "text": "test",
        })
        assert response.status_code == 400
