"""
Рівень 2 — Тести генераторів та фабрики (generators.py).
"""
import pytest
from generators import (
    ChaosFactory,
    LorenzSystemGenerator,
    RosslerSystemGenerator,
    ChuaSystemGenerator,
    DuffingSystemGenerator,
    VanDerPolSystemGenerator,
    ForcedPendulumSystemGenerator,
    IChaosGenerator,
)
from conftest import ALL_SYSTEM_CONFIGS, LORENZ_PARAMS


class TestChaosFactory:
    """Тести фабрики ChaosFactory."""

    @pytest.mark.parametrize("system_type, params", ALL_SYSTEM_CONFIGS,
                             ids=[c[0] for c in ALL_SYSTEM_CONFIGS])
    def test_create_all_systems(self, system_type, params):

        factory = ChaosFactory()
        gen = factory.create_generator(system_type, params, "chars")
        assert isinstance(gen, IChaosGenerator)

    def test_unknown_system_raises(self):

        factory = ChaosFactory()
        with pytest.raises(ValueError, match="Unknown system type"):
            factory.create_generator("henon", {}, "chars")

    def test_lorenz_creates_correct_class(self):
        factory = ChaosFactory()
        gen = factory.create_generator("lorenz", LORENZ_PARAMS, "bytes")
        assert isinstance(gen, LorenzSystemGenerator)

    EXPECTED_CLASSES = [
        ("lorenz", LorenzSystemGenerator),
        ("rossler", RosslerSystemGenerator),
        ("chua", ChuaSystemGenerator),
        ("duffing", DuffingSystemGenerator),
        ("pol", VanDerPolSystemGenerator),
        ("forced", ForcedPendulumSystemGenerator),
    ]

    @pytest.mark.parametrize("system_type, expected_class", EXPECTED_CLASSES,
                             ids=[e[0] for e in EXPECTED_CLASSES])
    def test_factory_creates_correct_class(self, system_type, expected_class):
        factory = ChaosFactory()
        params = dict(ALL_SYSTEM_CONFIGS)[system_type]
        gen = factory.create_generator(system_type, params, "chars")
        assert type(gen) is expected_class


class TestGeneratorInterface:


    def test_get_sequence_returns_list(self, make_generator):
        gen = make_generator("lorenz", LORENZ_PARAMS, "chars")
        result = gen.get_sequence(50)
        assert isinstance(result, list)
        assert len(result) == 50

    def test_state_changes_between_calls(self, make_generator):
        gen = make_generator("lorenz", LORENZ_PARAMS, "chars")
        result1 = gen.get_sequence(10)
        result2 = gen.get_sequence(10)
        assert result1 != result2

    def test_string_params_converted_to_float(self):

        factory = ChaosFactory()
        string_params = {k: str(v) for k, v in LORENZ_PARAMS.items()}
        gen = factory.create_generator("lorenz", string_params, "chars")
        result = gen.get_sequence(10)
        assert len(result) == 10

    def test_missing_param_raises_key_error(self):
        factory = ChaosFactory()
        incomplete_params = {"logisticXLorenz": 0.3}  # відсутні lorenzX, lorenzY, lorenzZ
        with pytest.raises(KeyError):
            factory.create_generator("lorenz", incomplete_params, "chars")
