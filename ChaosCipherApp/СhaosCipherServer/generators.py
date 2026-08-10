from abc import ABC, abstractmethod
from typing import List, Dict, Any
from chaosSystems.chuaSystem import get_logistic_chua_sequence
from chaosSystems.duffingSystem import get_logistic_duffing_sequence
from chaosSystems.forcedPendulum import get_logistic_forced_pendulum_sequence
from chaosSystems.lorenzSystem import get_logistic_lorenz_sequence
from chaosSystems.rosslerSystem import get_logistic_rossler_sequence
from chaosSystems.vanDerPolSystem import get_logistic_van_der_pol_sequence

class IChaosGenerator(ABC):
    @abstractmethod
    def get_sequence(self, length: int) -> List[Any]:pass

class LorenzSystemGenerator(IChaosGenerator):
    def __init__(self, params, mode):
        self.logistic_x= float(params["logisticXLorenz"])
        self.lorenz_x = float(params["lorenzX"])
        self.lorenz_y = float(params["lorenzY"])
        self.lorenz_z = float(params["lorenzZ"])
        self.mode = mode
    def get_sequence(self, length: int) -> List[Any]:
        is_sha = True if self.mode == "bytes" else False
        new_logistic_x, new_lorenz_x, new_lorenz_y, new_lorenz_z, result= get_logistic_lorenz_sequence(length, self.logistic_x, self.lorenz_x, self.lorenz_y, self.lorenz_z, is_sha)
        self.logistic_x = new_logistic_x
        self.lorenz_x = new_lorenz_x
        self.lorenz_y = new_lorenz_y
        self.lorenz_z = new_lorenz_z
        print(new_logistic_x, new_lorenz_x, new_lorenz_y, new_lorenz_z)
        return result

class RosslerSystemGenerator(IChaosGenerator):
    def __init__(self, params, mode):
        self.logistic_x= float(params["logisticXRossler"])
        self.rossler_x = float(params["rosslerX"])
        self.rossler_y = float(params["rosslerY"])
        self.rossler_z = float(params["rosslerZ"])
        self.mode = mode
    def get_sequence(self, length: int) -> List[Any]:
        is_sha = True if self.mode == "bytes" else False
        new_logistic_x, new_rossler_x, new_rossler_y, new_rossler_z, result = get_logistic_rossler_sequence(length, self.logistic_x, self.rossler_x, self.rossler_y, self.rossler_z, is_sha)
        self.logistic_x = new_logistic_x
        self.rossler_x = new_rossler_x
        self.rossler_y = new_rossler_y
        self.rossler_z = new_rossler_z
        return result

class ChuaSystemGenerator(IChaosGenerator):
    def __init__(self, params, mode):
        self.logistic_x= float(params["logisticXChua"])
        self.chua_x = float(params["chuaX"])
        self.chua_y = float(params["chuaY"])
        self.chua_z = float(params["chuaZ"])
        self.mode = mode
    def get_sequence(self, length: int) -> List[Any]:
        is_sha = True if self.mode == "bytes" else False
        new_logistic_x, new_chua_x, new_chua_y, new_chua_z, result = get_logistic_chua_sequence(length, self.logistic_x, self.chua_x, self.chua_y, self.chua_z, is_sha)
        self.logistic_x = new_logistic_x
        self.chua_x = new_chua_x
        self.chua_y = new_chua_y
        self.chua_z = new_chua_z
        return result

class DuffingSystemGenerator(IChaosGenerator):
    def __init__(self, params, mode):
        self.logistic_x= float(params["logisticXDuffing"])
        self.duffing_x = float(params["duffingX"])
        self.duffing_y = float(params["duffingY"])
        self.duffing_t = float(params["duffingT"])
        self.mode = mode
    def get_sequence(self, length: int) -> List[Any]:
        is_sha = True if self.mode == "bytes" else False
        new_logistic_x, new_duffing_x, new_duffing_y, new_duffing_t, result = get_logistic_duffing_sequence(length, self.logistic_x, self.duffing_x, self.duffing_y, self.duffing_t, is_sha)
        self.logistic_x = new_logistic_x
        self.duffing_x = new_duffing_x
        self.duffing_y = new_duffing_y
        self.duffing_t = new_duffing_t
        return result
 
class VanDerPolSystemGenerator(IChaosGenerator):
    def __init__(self, params, mode):
        self.logistic_x= float(params["logisticXPol"])
        self.pol_x = float(params["polX"])
        self.pol_y = float(params["polY"])
        self.pol_t = float(params["polT"])
        self.mode = mode
    def get_sequence(self, length: int) -> List[Any]:
        is_sha = True if self.mode == "bytes" else False
        new_logistic_x, new_pol_x, new_pol_y, new_pol_t, result = get_logistic_van_der_pol_sequence(length, self.logistic_x, self.pol_x, self.pol_y, self.pol_t, is_sha)

        self.logistic_x = new_logistic_x
        self.pol_x = new_pol_x
        self.pol_y = new_pol_y
        self.pol_t = new_pol_t
        return result
 
class ForcedPendulumSystemGenerator(IChaosGenerator):
    def __init__(self, params, mode):
        self.logistic_x= float(params["logisticXForced"])
        self.forced_x = float(params["forcedX"])
        self.forced_y = float(params["forcedY"])
        self.forced_t = float(params["forcedT"])
        self.mode = mode
    def get_sequence(self, length: int) -> List[Any]:
        is_sha = True if self.mode == "bytes" else False
        new_logistic_x, new_forced_x, new_forced_y, new_forced_t, result  = get_logistic_forced_pendulum_sequence(length, self.logistic_x, self.forced_x, self.forced_y, self.forced_t, is_sha)
        self.logistic_x = new_logistic_x
        self.forced_x = new_forced_x
        self.forced_y = new_forced_y
        self.forced_t = new_forced_t
        return result

class TestChaosGenerator(IChaosGenerator):
    def __init__(self):pass
    def get_sequence(self, length: int) -> List[int]:
        #C1 = np.arange(length, 0, -1)
        C1 = get_logistic_lorenz_sequence(length, 0.2, 1, 1, 1, False)
        return C1

class ChaosFactory():
    _registry = {
        "lorenz": LorenzSystemGenerator,
        "rossler": RosslerSystemGenerator,
        "chua": ChuaSystemGenerator,
        "duffing": DuffingSystemGenerator,
        "pol": VanDerPolSystemGenerator,
        "forced": ForcedPendulumSystemGenerator,
    }    
    def create_generator(self, system_type: str, params: Dict, mode: str):
        try:
            generator_class = self._registry[system_type]
        except KeyError:
            raise ValueError(f"Unknown system type: {system_type}")
        return generator_class(params, mode)
