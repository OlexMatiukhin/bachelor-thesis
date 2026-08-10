
import math
import pytest
import numpy as np

from chaosSystems.lorenzSystem import get_logistic_lorenz_sequence, logistic_generator
from chaosSystems.rosslerSystem import get_logistic_rossler_sequence
from chaosSystems.chuaSystem import get_logistic_chua_sequence
from chaosSystems.duffingSystem import get_logistic_duffing_sequence
from chaosSystems.vanDerPolSystem import get_logistic_van_der_pol_sequence
from chaosSystems.forcedPendulum import get_logistic_forced_pendulum_sequence

SYSTEMS = [
    pytest.param(get_logistic_lorenz_sequence, 1.0, 1.0, 1.0, id="lorenz"),
    pytest.param(get_logistic_rossler_sequence, 1.0, 1.0, 1.0, id="rossler"),
    pytest.param(get_logistic_chua_sequence, 0.1, 0.0, 0.0, id="chua"),
    pytest.param(get_logistic_duffing_sequence, 0.1, 0.0, 0.0, id="duffing"),
    pytest.param(get_logistic_van_der_pol_sequence, 0.1, 0.0, 0.0, id="van_der_pol"),
    pytest.param(get_logistic_forced_pendulum_sequence, 0.1, 0.0, 0.0, id="forced_pendulum"),
]

LOGISTIC_X = 0.3


@pytest.mark.parametrize("seq_func, x0, y0, z0", SYSTEMS)
class TestChaosSystemCommon:
    """Загальні тести для всіх 6 хаотичних систем."""

    def test_determinism(self, seq_func, x0, y0, z0):
        """Два виклики з однаковими параметрами → ідентичний результат."""
        _, _, _, _, result1 = seq_func(50, LOGISTIC_X, x0, y0, z0, False)
        _, _, _, _, result2 = seq_func(50, LOGISTIC_X, x0, y0, z0, False)
        assert result1 == result2

    @pytest.mark.parametrize("length", [500])
    def test_sequence_length(self, seq_func, x0, y0, z0, length):
        """Довжина результату точно дорівнює запрошеній."""
        _, _, _, _, result = seq_func(length, LOGISTIC_X, x0, y0, z0, False)
        assert len(result) == length



    def test_state_updated(self, seq_func, x0, y0, z0):
        """Повернутий стан відрізняється від початкового."""
        new_w, new_x, new_y, new_z, _ = seq_func(10, LOGISTIC_X, x0, y0, z0, False)
        assert new_w != LOGISTIC_X
        # Хоча б одна з координат має змінитися
        assert not (new_x == x0 and new_y == y0 and new_z == z0)

    def test_sensitivity_to_initial_conditions(self, seq_func, x0, y0, z0):
        """Мінімальна зміна logistic_x → розбіжність послідовностей."""
        _, _, _, _, result1 = seq_func(100, LOGISTIC_X, x0, y0, z0, False)
        _, _, _, _, result2 = seq_func(100, LOGISTIC_X, x0, y0, z0+ 1e-5, False)
        # Перші елементи близькі, але далі — розходяться
        diffs = sum(1 for a, b in zip(result1, result2) if abs(a - b) > 1e-6)
        assert diffs > 10, "Послідовності занадто схожі — чутливість не виявлена"
    

    def test_finite_values(self, seq_func, x0, y0, z0):
        """100000 ітерацій без NaN/Inf."""
        _, _, _, _, result = seq_func(100000, LOGISTIC_X, x0, y0, z0, False)
        for val in result:
            assert math.isfinite(val), f"Виявлено не-фінітне значення: {val}"

    def test_dont_fall_into_circles(self, seq_func, x0, y0, z0):
        _, _, _, _, result = seq_func(100000, LOGISTIC_X, x0, y0, z0, False)
        seen = set()
        for i, val in enumerate(result):
            assert val not in seen, f"Цикл на елементі {i}"
            seen.add(val)


class TestLogisticMap:


    def test_stays_in_unit_interval(self):
        x = 0.3
        for _ in range(10_000):
            x = logistic_generator(x)
            assert 0.0 < x < 1.0, f"Вихід за межі: x={x}"


    def test_invalid_logistic_x_zero(self):
        with pytest.raises(ValueError, match="logisticX must be in"):
            get_logistic_lorenz_sequence(10, 0.0, 1.0, 1.0, 1.0, False)

    def test_invalid_logistic_x_one(self):
        with pytest.raises(ValueError, match="logisticX must be in"):
            get_logistic_lorenz_sequence(10, 1.0, 1.0, 1.0, 1.0, False)
