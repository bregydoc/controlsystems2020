import sympy as sp
import numpy as np
from matplotlib import pyplot as plt
from mpmath import chop


def find_roots(gs: sp.Expr):
    results: [complex] = []

    s = sp.var("s")

    for ki in np.arange(0.001, 10, 0.1):
        # ki = 0.1
        sn0 = 0.1j
        for i in range(0, 10):
            num = complex((1+ki*gs.subs(s, sn0)).n(chop=True))
            den = complex(sp.diff(gs, s).subs(s, sn0).n(chop=True))
            sn = sn0 - num/ki/den
            sn0 = sn
        results.append(sn0)
    plt.plot(np.imag(results), np.real(results))
    plt.grid()
    plt.show()


s = sp.var("s")
np.poly([1, 0, 0, 0, 1, 1])
g = s**5 + s + 1
find_roots(g)