from initialize import *
import matplotlib.pyplot as plt
import energy, interpolate, field, dynamics, figures, specKernel

picNum = 0
Shat, K = specKernel.specKernel()
for it in range(NT):
    print(it)
    xp = dynamics.toPeriodic(xp, L)
    if it % 25 == 1 and picNum < 16:
        picNum = picNum + 1
        plt.subplot(4, 4, picNum)
        figures.phaseSpace(xp, vp)
        plt.title('$t$=%s' % str(np.round(it * DT, 4)))
    rhoHat = interpolate.specInterpolate(xp, Shat, wp)
    phiHat, EgHat = field.fieldInFourier(rhoHat)
    vp, kinetic = dynamics.accelInFourier(vp, xp, it, EgHat, Shat, wp)
    xp, wp = dynamics.move(xp, vp, wp)
    potential = energy.potential(rhoHat, phiHat)
    Ek.append(kinetic)
    Ep.append(potential)
    E.append(kinetic + potential)
    momentum.append(sum(Q * vp / QM))
    phiMax.append(np.max(np.fft.ifft(phiHat) * NG / L))
plt.show()
figures.landauDecayFig(phiMax)
plt.show()
