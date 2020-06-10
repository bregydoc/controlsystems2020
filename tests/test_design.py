import unittest
import sympy as sp
import numpy as np
import control as ct
from control2020 import design, core


class TestingDesignAlgorithms(unittest.TestCase):
    def test_pid(self):
        s = sp.var("s")
        gs = 1 / s / (s + 1) / (s + 3)
        sys = core.symbolic_transfer_function(gs)
        ts = 11.5
        po = 0.5

        controller = design.pid_with_root_placing(sys, po, ts)
        expected_controller = core.symbolic_transfer_function((6.203*s**2 + 5.229*s + 1.102) / s)

        self.assertLessEqual(np.mean(np.array(expected_controller.num) - np.array(controller.num)), 1e-3)
        self.assertLessEqual(np.mean(np.array(expected_controller.den) - np.array(controller.den)), 1e-3)

    def test_lead_compensator(self):
        s = sp.var("s")
        sys = 10/s/(s+1)

        expected_controller = core.symbolic_transfer_function((0.2953*s + 0.3249)/(0.3196*s + 1))

        controller = design.lead_compensator_with_root_placing(sys, 16.3, 2.67, -1.1)

        self.assertLessEqual(np.mean(np.array(expected_controller.num) - np.array(controller.num)), 1e-3)
        self.assertLessEqual(np.mean(np.array(expected_controller.den) - np.array(controller.den)), 1e-3)

        expected_po = 20
        expected_ts = 5

        controller = design.lead_compensator_with_root_placing(sys,
                                                               expected_po, expected_ts, -1,
                                                               auto_tune=True)

        feedback_sys = ct.feedback(controller*core.symbolic_transfer_function(sys), 1)
        info = ct.step_info(feedback_sys)
        self.assertLessEqual(info["SettlingTime"] - expected_ts, 1e-2)
        self.assertLessEqual(info["Overshoot"] - expected_po, 1e-2)


if __name__ == '__main__':
    unittest.main()
