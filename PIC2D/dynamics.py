from initialize import QM, L, DT, findsource
from energy import kinetic
import numpy as np
import finufft

def accelerate(vp, it, M, E, wp):
    a = np.transpose(M * E) * QM / wp
    return push(vp, a, it)


def accelInFourier(xp, EgHat, Shat, wp):
    coeff1 = np.conjugate(EgHat[0] * Shat)
    a1 = np.real(finufft.nufft2d2(xp[0] * 2 * np.pi / L[0], xp[1] * 2 * np.pi / L[1], coeff1, eps=1e-12, modeord=1) * QM / (L[0] * L[1] * wp))
    coeff2 = np.conjugate(EgHat[1] * Shat)
    a2 = np.real(finufft.nufft2d2(xp[0] * 2 * np.pi / L[0], xp[1] * 2 * np.pi / L[1], coeff2, eps=1e-12, modeord=1) * QM / (L[1] * L[0] * wp))
    return np.array([a1, a2])


def push(vp, a, it):
    if it == 0:
        return vp + a * DT / 2, kinetic(vp + a * DT)
    else:
        return vp + a * DT, kinetic(vp + a * DT / 2)


def move(xp, vp, wp, it=None):
    if wp is 1:
        return xp + vp * DT, 1
    else:
        return xp + vp * DT, wp + DT * findsource(xp + vp * DT / 2, vp, L, it + 0.5, DT)


def toPeriodic(x, L, discrete=False):
    out = (x < 0)
    x[out] = x[out] + L
    if discrete:
        out = (x > L - 1)
    else:
        out = (x >= L)
    x[out] = x[out] - L
    return x

def toPeriodicND(x, L, dim=2, discrete=False):
    for i in range(dim):
        x[i] = toPeriodic(x[i], L[i], discrete)
    return x

x = np.array([[1,2,3],[4,5,6],[7,8,9]])
x[:,1:] = np.flip(x[:,1:], 1)
print(x)
# x = np.append(np.transpose([x[:, 0]]), np.flip(x[:, 1:], 1), axis=1)
# print(x)
# x = np.append([x[0, :]], np.flip(x[1:, :], 0), axis=0)
# print(x)