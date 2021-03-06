import control as ct
import numpy as np


def states_tracker(sys, poles=None, po=None, ts=None, extra_poles=[]):
    pa = np.concatenate([sys.A, np.zeros(shape=(sys.A.shape[0], 1))], axis=1)
    pb = np.concatenate([-sys.C, [[0]]], axis=1)

    ag = np.concatenate([pa, pb])
    bg = np.concatenate([sys.B, [[0]]])
    cg = np.concatenate([sys.C, [[1e-6]]], axis=1)
    dg = [[0]]

    gg = ct.ss(ag, bg, cg, dg)

    mc = ct.ctrb(gg.A, gg.B)

    rank = np.linalg.matrix_rank(mc)

    print(f"rank= {rank}")
    if rank < sys.A.shape[0]:
        raise BaseException("invalid matrix, it's not full controllable")

    final_poles = []

    if poles is not None:
        final_poles = poles

    if po is not None and ts is not None:
        log_po = np.log(100 / po)
        psi = log_po / np.sqrt(np.pi ** 2 + log_po ** 2)
        wn = 4 / psi / ts

        s1 = -psi * wn + 1j * wn * np.sqrt(1 - psi ** 2)
        s2 = -psi * wn - 1j * wn * np.sqrt(1 - psi ** 2)

        final_poles.append(s1)
        final_poles.append(s2)

    for p in extra_poles:
        final_poles.append(p)

    total_poles = len(final_poles)

    if total_poles < rank:
        raise BaseException(f"you have {total_poles} but you need {rank} to implement a FSFB")

    kk = ct.acker(ag, bg, final_poles)
    k = kk[0, :sys.A.shape[0]]
    ki = -kk[0, -1]

    print("k=", k)
    print("ki=", ki)

    pa = np.concatenate([sys.A - sys.B * k, sys.B * ki], axis=1)
    pb = np.concatenate([-sys.C, [[1e-6]]], axis=1)

    ak = np.concatenate([pa, pb], axis=0)
    bk = np.concatenate([np.zeros((sys.A.shape[0], 1)), [[1]]])
    ck = np.concatenate([sys.C, [[1e-6]]], axis=1)
    dk = np.array([[0]])

    return ct.ss(ak, bk, ck, dk)

# TODO: Optimizeeeeeeeee

def tracker_with_observer(sys, poles=None, po=None, ts=None, extra_poles=[]):
    pa = np.concatenate([sys.A, np.zeros(shape=(sys.A.shape[0], 1))], axis=1)
    pb = np.concatenate([-sys.C, [[0]]], axis=1)

    ao = np.concatenate([pa, pb])
    bo = np.concatenate([sys.B, [[1e-8]]])

    mc = ct.ctrb(ao, bo)

    rank = np.linalg.matrix_rank(mc)

    print(f"rank= {rank}")
    if rank < sys.A.shape[0]:
        raise BaseException("invalid matrix, it's not full controllable")

    final_poles = []

    if poles is not None:
        final_poles = poles

    if po is not None and ts is not None:
        log_po = np.log(100 / po)
        psi = log_po / np.sqrt(np.pi ** 2 + log_po ** 2)
        wn = 4 / psi / ts

        s1 = -psi * wn + 1j * wn * np.sqrt(1 - psi ** 2)
        s2 = -psi * wn - 1j * wn * np.sqrt(1 - psi ** 2)

        final_poles.append(s1)
        final_poles.append(s2)

    for p in extra_poles:
        final_poles.append(p)

    total_poles = len(final_poles)

    if total_poles < rank:
        raise BaseException(f"you have {total_poles} but you need {rank} to implement a FSFB")

    kk = ct.acker(ao, bo, final_poles)
    k = kk[0, :sys.A.shape[0]]
    ki = -kk[0, -1]

    print("k=", k)
    print("ki=", ki)

    mo = ct.obsv(sys.A, sys.C);
    obs_rank = np.linalg.matrix_rank(mo)

    print("obs_rank=", obs_rank)

    final_poles_obs = 5* final_poles[:-1]

    l = ct.acker(sys.A.T, sys.C.T, final_poles_obs)
    l = l.T
    print("")
    print("L=")
    print(l)

    pa = np.concatenate([sys.A, - sys.B * k, sys.B * ki], axis=1)
    pb = np.concatenate([l * sys.C, sys.A - sys.B * k - l * sys.C, sys.B * ki], axis=1)
    pc = np.concatenate([-sys.C, np.zeros((1, sys.A.shape[0])), [[0]]], axis=1)

    alc = np.concatenate([pa, pb, pc], axis=0)
    blc = np.concatenate([np.zeros((sys.A.shape[0], 1)), np.zeros((sys.A.shape[0], 1)), [[1]]])
    clc = np.concatenate([sys.C, np.zeros((1, sys.A.shape[0])), [[1e-6]]], axis=1)
    dlc = np.array([[0]])

    return ct.ss(alc, blc, clc, dlc)