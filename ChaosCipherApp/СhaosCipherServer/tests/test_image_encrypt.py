"""
Рівень 3B — Тести шифрування зображень (encrypt_alg/image_encrypt_server.py).
"""
import pytest
import numpy as np
from io import BytesIO
import PIL.Image as Image
import copy
import pytest
import numpy as np
from io import BytesIO
import PIL.Image as Image
from generators import ChaosFactory
from conftest import ALL_SYSTEM_CONFIGS
from encrypt_alg.image_encrypt_server import (
    encrypt_image, decrypt_image,
    scrambling, scrambling_decryp,
    diffusion, diffusion_decrypt,
    make_header, parse_header,
    embed_header_rgb_in_padding, extract_header,
    rank, get_FSM, log_integer_exponent,
    get_number_iterations_and_size_by_power,
    add_element_to_pixels_matrix, remove_additional_elements_from_matrix,
)
from conftest import LORENZ_PARAMS
def _pixels(image_bytes: bytes) -> np.ndarray:
    return np.array(Image.open(BytesIO(image_bytes)).convert("RGB"))
def _expand_sensitivity_cases():

    cases = []
    for system_name, base_params in ALL_SYSTEM_CONFIGS:
        for param_name, value in base_params.items():
            if isinstance(value, (int, float)):
                cases.append(
                    pytest.param(
                        system_name,
                        base_params,
                        param_name,
                        id=f"{system_name}-{param_name}",
                    )
                )
    return cases

FACTORY = ChaosFactory()


def _make_gen(system_name, params, mode=""):
    return FACTORY.create_generator(system_name, params, mode)


class TestImageRoundtrip:

    def test_roundtrip_3x5(self, test_image_bytes):
        """Шифрування - дешифрування 3×5 PNG зображення."""
        gen_enc = _make_gen()
        gen_dec = _make_gen()
        encrypted = encrypt_image(test_image_bytes, gen_enc)
        decrypted = decrypt_image(encrypted, gen_dec)
        # Порівнюємо пікселі
        orig = np.array(Image.open(BytesIO(test_image_bytes)).convert("RGB"))
        rest = np.array(Image.open(BytesIO(decrypted)).convert("RGB"))
        np.testing.assert_array_equal(orig, rest)

    def test_encrypted_differs_from_original(self, test_image_bytes):
        encrypted = encrypt_image(test_image_bytes, _make_gen())
        assert encrypted != test_image_bytes

    def test_invalid_data_enc(self):
        with pytest.raises((ValueError, Exception)):
            decrypt_image(None, _make_gen())
    def test_invalid_data_dec(self):
        with pytest.raises((ValueError, Exception)):
            decrypt_image(test_image_bytes, _make_gen())

@pytest.mark.parametrize(
    "system_name, base_params, param_name",
    _expand_sensitivity_cases(),
)
def test_parameter_sensitivity(
    self, system_name, base_params, param_name, test_image_bytes
):


    gen_enc = _make_gen(system_name, base_params)
    encrypted = encrypt_image(test_image_bytes, gen_enc)

    orig_pixels = _pixels(test_image_bytes)

    perturbed = copy.deepcopy(base_params)
    perturbed[param_name] = float(perturbed[param_name]) + 1e-6

    gen_dec_wrong = _make_gen(system_name, perturbed)

    try:
        decrypted_wrong = decrypt_image(encrypted, gen_dec_wrong)

    except ValueError:

        return

    except Exception as e:
        pytest.fail(
            f"System '{system_name}', param '{param_name}': "
            f"неожиданная ошибка вместо ValueError: {type(e).__name__}: {str(e)}"
        )

    wrong_pixels = _pixels(decrypted_wrong)

    assert orig_pixels.shape == wrong_pixels.shape, (
        f"System '{system_name}', param '{param_name}': "
        f"изменился размер изображения после неверной расшифровки"
    )

    pixel_changed = np.any(orig_pixels != wrong_pixels, axis=2)
    npcr = np.count_nonzero(pixel_changed) / pixel_changed.size * 100

    diff = np.abs(
        orig_pixels.astype(np.int16) - wrong_pixels.astype(np.int16)
    )
    uaci = np.mean(diff) / 255 * 100

    assert npcr > 99.0 and uaci > 20.0, (
        f"System '{system_name}' недостаточно чувствительна "
        f"к параметру '{param_name}' при изменении на 1e-6. "
        f"decrypt_image не выбросил ValueError, "
        f"а изображение осталось слишком похожим на оригинал. "
        f"NPCR={npcr:.4f}%, UACI={uaci:.4f}%"
    )

