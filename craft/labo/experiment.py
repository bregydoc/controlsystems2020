from typing import Dict, Tuple, List, Union
from .systems import System, TF
import numpy as np
from dataclasses import dataclass
import control as ct


@dataclass
class Variable:
    kind: str # possible: once, array, range
    start: float = 0
    end: float = 1
    steps: float = 1
    fixed: Union[float, list] = None


class BasicSystem(System):
    def __init__(self, g: TF, k: TF = 1, h: TF = 1):
        super().__init__(g, k, h, 0, 0)


class BasicExperiment:
    def __init__(self, system: BasicSystem):
        self.system: BasicSystem = system
        self.variables: List[Variable] = []

    def add_variable(self, var: Variable):
        self.variables.append(var)

    def render_step(self) -> Dict:
        data = []
        for i in np.linspace(-0.5, 0.5, 10):
            sys = self.system.copy()
            plant = sys.G
            print(plant.num[0][0], [plant.den[0][0][0] + i, *plant.den[0][0][1:]])
            new_plant = ct.TransferFunction(plant.num[0][0], [plant.den[0][0][0] + i, *plant.den[0][0][1:]])
            sys.update(g=new_plant)
            t, y = sys.step()
            data.append({"x": t, "y": y, "type": "line", "name": "system"})
        return {
            "data": data,
            "layout": {
                "title": "Step Response of System",
                "xaxis": {"title": "Time (s)"},
                "yaxis": {"title": "Amplitude"}
            }
        }

    def render_bode(self) -> Tuple[Dict, Dict]:
        mag, phase, omega = self.system.bode_close()

        phase = phase * 180. / np.pi
        mag = 20. * np.log10(mag)

        return {
            "data": [
                {"x": omega, "y": mag, "type": "line", "name": "Magnitude"},
            ],
            "layout": {
                "title": "Bode Plot",
                "xaxis": {"type": "log"}, # "title": "Frequency"
                "yaxis": {"title": "Magnitude (dB)"},
                "margin": {"t": 40, "b": 30},
                "height": 200
            }
        }, {
            "data": [
                {"x": omega, "y": phase, "type": "line", "name": "Phase"}
            ],
            "layout": {
                "xaxis": {"type": "log", "title": "Frequency"},
                "yaxis": {"title": "Phase (deg)"},
                "margin": {"t": 20, "b": 40},
                "height": 200
            }
        }