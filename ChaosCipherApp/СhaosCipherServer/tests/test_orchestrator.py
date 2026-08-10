"""
Рівень 5 — Тести оркестратора (orchestrator.py).
"""
import pytest
from orchestrator import CryptoOrchestrator
from conftest import LORENZ_PARAMS, ROSSLER_PARAMS, ALL_SYSTEM_CONFIGS


@pytest.fixture
def orchestrator():
    return CryptoOrchestrator()


class TestOrchestratorText:

    def test_text_encrypt_decrypt_chars(self, orchestrator):
        text = "Тестовий текст для оркестратора"
        encrypted = orchestrator.execute_request(
            system_type="lorenz", system_params=LORENZ_PARAMS,
            crypt_method="text", mode="chars",
            content=text, process_type="encrypt",
        )
        decrypted = orchestrator.execute_request(
            system_type="lorenz", system_params=LORENZ_PARAMS,
            crypt_method="text", mode="chars",
            content=encrypted, process_type="decrypt",
        )
        assert decrypted == text

    def test_text_encrypt_decrypt_bits(self, orchestrator):
        text = "Binary mode test"
        encrypted = orchestrator.execute_request(
            system_type="lorenz", system_params=LORENZ_PARAMS,
            crypt_method="text", mode="bytes",
            content=text, process_type="encrypt",
        )
        decrypted = orchestrator.execute_request(
            system_type="lorenz", system_params=LORENZ_PARAMS,
            crypt_method="text", mode="bytes",
            content=encrypted, process_type="decrypt",
        )
        assert decrypted == text


class TestOrchestratorValidation:

    def test_unknown_crypt_method(self, orchestrator):
        with pytest.raises(ValueError, match="Unknown crypt_method"):
            orchestrator.execute_request(
                system_type="lorenz", system_params=LORENZ_PARAMS,
                crypt_method="video", mode="chars",
                content="test", process_type="encrypt",
            )

    def test_unknown_system_type(self, orchestrator):
        with pytest.raises(ValueError, match="Unknown system type"):
            orchestrator.execute_request(
                system_type="henon", system_params={},
                crypt_method="text", mode="chars",
                content="test", process_type="encrypt",
            )


class TestOrchestratorIsolation:

    def test_same_params_same_result(self, orchestrator):
        """Два виклики з однаковими параметрами → однаковий результат."""
        text = "Isolation test"
        enc1 = orchestrator.execute_request(
            system_type="lorenz", system_params=LORENZ_PARAMS,
            crypt_method="text", mode="chars",
            content=text, process_type="encrypt",
        )
        enc2 = orchestrator.execute_request(
            system_type="lorenz", system_params=LORENZ_PARAMS,
            crypt_method="text", mode="chars",
            content=text, process_type="encrypt",
        )
        assert enc1 == enc2

    @pytest.mark.parametrize("system_type, params", ALL_SYSTEM_CONFIGS,
                             ids=[c[0] for c in ALL_SYSTEM_CONFIGS])
    def test_all_systems_text_roundtrip(self, orchestrator, system_type, params):
        """Roundtrip тексту через оркестратор для кожної системи."""
        text = "Test all systems"
        encrypted = orchestrator.execute_request(
            system_type=system_type, system_params=params,
            crypt_method="text", mode="chars",
            content=text, process_type="encrypt",
        )
        decrypted = orchestrator.execute_request(
            system_type=system_type, system_params=params,
            crypt_method="text", mode="chars",
            content=encrypted, process_type="decrypt",
        )
        assert decrypted == text
