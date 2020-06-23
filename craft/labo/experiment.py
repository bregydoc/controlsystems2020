from typing import Dict, Tuple, List, Union
from .systems import System, TF
import numpy as np
import sympy as sp
from dataclasses import dataclass
import control as ct


@dataclass
class Variable:
    name: str
    kind: str  # possible: once, array, range
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

    def new_system(self, var_name: str, var_value: str, g: str = None, k: str = None, h: str = None) -> BasicSystem:
        new_sys = self.system.copy()
        g_val, k_val, h_val = None, None, None
        if g is not None:
            g_val = g.replace(var_name, str(var_value))
        if k is not None:
            k_val = k.replace(var_name, str(var_value))
        if h is not None:
            h_val = h.replace(var_name, str(var_value))

        new_sys.update(g=g_val, k=k_val, h=h_val)
        return new_sys

    def calculate_variations(self, g: str = None, k: str = None, h: str = None) -> List[Tuple[str, str, BasicSystem]]:
        systems: List[Tuple[str, str, BasicSystem]] = []
        for var in self.variables:
            if var.kind == "once":
                new_sys = self.new_system(var.name, str(var.fixed), g, k, h)
                systems.append((var.name, str(var.fixed), new_sys))
            elif var.kind == "array":
                if type(var.fixed) == list:
                    for val in var.fixed:
                        new_sys = self.new_system(var.name, str(val), g, k, h)
                        systems.append((var.name, str(val), new_sys))
            elif var.kind == "range":
                for val in np.arange(var.start, var.end, var.steps):
                    new_sys = self.new_system(var.name, str(val), g, k, h)
                    systems.append((var.name, str(val), new_sys))
            else:
                raise BaseException("invalid kind of variable")

        return systems

    def render_step(self, g: str = None, k: str = None, h: str = None) -> Dict:
        data: List[Dict] = []

        variations = self.calculate_variations(g, k, h)

        for i, variation in enumerate(variations):
            t, y = variation[2].step()
            # report = variation[2].step_report()
            data.append({"x": t, "y": y, "type": "line", "name": f"when {variation[0]}={variation[1]}"})
            # "text": f"RiseTime: {report['RiseTime']}\n" +
            # f"SettlingTime: {report['SettlingTime']}\n" +
            # f"SettlingMin: {report['SettlingMin']}\n" +
            # f"SettlingMax: {report['SettlingMax']}\n" +
            # f"Overshoot: {report['Overshoot']}\n" +
            # f"Undershoot: {report['Undershoot']}\n" +
            # f"Peak: {report['Peak']}\n" +
            # f"PeakTime: {report['PeakTime']}\n" +
            # f"SteadyStateValue: {report['SteadyStateValue']}\n",

        return {
            "data": data,
            "layout": {
                "title": "Step Response of System",
                "xaxis": {"title": "Time (s)"},
                "yaxis": {"title": "Amplitude"}
            }
        }

    def render_bode(self, g: str = None, k: str = None, h: str = None) -> Tuple[Dict, Dict]:
        magnitudes: List[Dict] = []
        phases: List[Dict] = []

        variations = self.calculate_variations(g, k, h)

        for i, variation in enumerate(variations):
            mag, phase, omega = variation[2].bode_close()
            magnitudes.append({"x": omega, "y": mag, "type": "line", "name": f"when {variation[0]}={variation[1]}"})
            phases.append({"x": omega, "y": phase, "type": "line", "name": f"when {variation[0]}={variation[1]}"})

        return {
                   "data": magnitudes,
                   "layout": {
                       "title": "Bode Plot",
                       "xaxis": {"type": "log"},  # "title": "Frequency"
                       "yaxis": {"title": "Magnitude (dB)"},
                       "margin": {"t": 40, "b": 30},
                       "height": 200
                   }
               }, {
                   "data": phases,
                   "layout": {
                       "xaxis": {"type": "log", "title": "Frequency"},
                       "yaxis": {"title": "Phase (deg)"},
                       "margin": {"t": 20, "b": 40},
                       "height": 200
                   }
               }
