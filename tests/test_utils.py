import sympy as sp
import control as ct
import numpy as np
import unittest
from control2020 import core
import math


class TestingUtils(unittest.TestCase):
    def testing_basic_symbolic_transfer_function(self):
        s = sp.var("s")

        tf = (1+s)/(2+s)/(s+3)
        result = ct.TransferFunction([1, 1], [1, 5, 6])

        sym_tf = core.symbolic_transfer_function(tf)

        equal_nums = np.array_equal(sym_tf.num, result.num)
        equal_dens = np.array_equal(sym_tf.den, result.den)

        self.assertEqual(equal_nums, True, "invalid result at convert from symbolic equation")
        self.assertEqual(equal_dens, True, "invalid result at convert from symbolic equation")

    def testing_complex_symbolic_transfer_function(self):
        s = sp.var("s")
        tf = 1/(s+2)/(3*s**2+3)/(5*s+1)/(17*s+4)/(13*s+8)/s

        expected = ct.TransferFunction([1], [3315, 10113, 11325, 12297, 8202, 2184, 192, 0])

        sym_tf = core.symbolic_transfer_function(tf)

        equal_nums = np.array_equal(sym_tf.num, expected.num)
        equal_dens = np.array_equal(sym_tf.den, expected.den)

        self.assertEqual(equal_nums, True)
        self.assertEqual(equal_dens, True)

    def testing_extract_characteristic_equation(self):
        s, k = sp.var("s K")

        sym_tf = 1/(1 + 2*s + 3*s**2)
        expected_eq, _ = sp.fraction(sp.factor(k*sym_tf + 1))
        c_eq = core.extract_characteristic_equation(g=sym_tf)

        self.assertEqual(c_eq, expected_eq, "invalid characteristic equation extraction")

        sym_tf = 1/(2 + 3*s)
        expected_eq, _ = sp.fraction(sp.factor(k * sym_tf * 2 + 1))

        c_eq = core.extract_characteristic_equation(g=sym_tf, k=k, h=2)

        self.assertEqual(c_eq, expected_eq, "invalid characteristic equation extraction")

    def testing_construct_poles(self):
        psi = 2.89e-01
        freq = 1.73e+00

        expected_poles = (-5.00e-01 + 1.66j, -5.00e-01 - 1.66j)
        poles = core.construct_poles(psi, freq)

        self.assertLessEqual(abs(poles[0] - expected_poles[0]), 4e-3)
        self.assertLessEqual(abs(poles[1] - expected_poles[1]), 4e-3)

        psi = 0.2364
        freq = 3.11

        expected_poles = (-0.7353 + 3.022j, -0.7353 - 3.022j)
        poles = core.construct_poles(psi, freq)

        self.assertLessEqual(abs(poles[0] - expected_poles[0]), 4e-3)
        self.assertLessEqual(abs(poles[1] - expected_poles[1]), 4e-3)

    def testing_from_quality_to_psi_wn(self):
        psi = 0.2364
        freq = 3.11

        po = 100 * math.exp(-psi*math.pi/(1-psi**2))
        ts = 4/psi/freq

        result_psi, result_wn = core.from_quality_to_psi_wn(po, ts)

        self.assertLessEqual(abs(result_psi - psi), 0.09)
        self.assertLessEqual(abs(result_wn - freq), 0.09)

    def testing_gain_to_poles(self):
        s = sp.var("s")
        g = (s+1)/(s+3)/(s+5)

        poles = core.gain_to_poles(g, gain=1.32)
        expected_poles = [-6.98, -2.33]

        for i, pole in enumerate(poles):
            self.assertLessEqual(abs(pole - expected_poles[i]), 0.01)

        g = 1/s/(s+2)/(s+5)/(s**2+4)

        poles = core.gain_to_poles(g, gain=178)
        expected_poles = [-5.31, -1.8 + 2.08j, -1.81 - 2.09j, 0.963 + 1.86j, 0.963 - 1.86j]

        for i, pole in enumerate(poles):
            self.assertLessEqual(abs(pole - expected_poles[i]), 0.01)

    def testing_pole_to_psi_wn(self):
        pole = 1 + 2j
        psi, wn = core.pole_to_psi_wn(pole)
        self.assertLessEqual(abs(psi - -4.47e-01), 0.01)
        self.assertLessEqual(abs(wn - 2.24), 0.01)

        pole = 2.7 + 3.1416j
        psi, wn = core.pole_to_psi_wn(pole)
        self.assertLessEqual(abs(psi - -6.52e-01), 0.01)
        self.assertLessEqual(abs(wn - 4.14), 0.01)

    def testing_point_report(self):
        point = 1 + 2j
        po, damp, freq = core.point_report(point, output=False)

        self.assertLessEqual(abs(po - 481), 1e3)
        self.assertLessEqual(abs(damp - -0.447), 1e3)
        self.assertLessEqual(abs(freq - 2.236), 1e3)

    def testing_step_report(self):
        sys = ct.TransferFunction([1], [1, 3, 2, 1])
        report_num = core.step_report(sys, output=False)
        self.assertNotEqual(report_num, None)

        s = sp.var("s")
        sys = 1/(s**3 + 3*s**2 + 2*s + 1)
        report_sym = core.step_report(sys, output=False)
        self.assertNotEqual(report_sym, None)

        for param in report_num.keys():
            self.assertLessEqual(abs(report_num[param] - report_sym[param]), 1e3)

    # def testing_plot_root_locus(self):
    #     core.plot_root_locus()

    def testing_find_point_in_root_locus(self):
        s = sp.var("s")
        poles = [-0.738 + 0.5j, -0.738 - 0.5j]

        g = 1/s/(s+3)/(s+2)

        founds = core.find_points_in_root_locus(g, poles)
        for found in founds:
            gain = found[0]
            self.assertLessEqual(abs(gain - 2.81), 1e2)

        poles = [-4.97]
        founds = core.find_points_in_root_locus(g, poles)
        for found in founds:
            gain = found[0]
            self.assertLessEqual(abs(gain - 29), 1e2)


if __name__ == '__main__':
    unittest.main()
