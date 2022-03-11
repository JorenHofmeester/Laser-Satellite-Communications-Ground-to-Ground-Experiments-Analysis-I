import math
import numpy as np
import pandas as pd
from scipy import integrate


def I0(W0, WLT):
    """

    :param W0: Beam radius
    :param WLT: Long-term spot size
    :return: Mean irradiance at beamcenter
    """
    return W0 ** 2 / WLT ** 2


def WLT(W, mu2d, Lambda, k, H, h0):
    """

    :param W: Diffractive beam radius
    :param mu2d: Turbulence factor
    :param Lambda:
    :param k: Wavenumber
    :param H: Altitude of receiver
    :param h0: Altitude of transmitter
    :return: Long-term spot size
    """
    return W * (1 + 4.35 * mu2d * Lambda ** (5 / 6) * k ** (7 / 6) * (H - h0) ** (5 / 6) * (
            (300 ** 2 + 10000 ** 2) ** (1 / 2) / 300) ** (11 / 6)) ** (1 / 2)


def W(W0, Theta0, Lambda0):
    """

    :param W0: Beam radius
    :param Theta0:
    :param Lambda0:
    :return: Diffractive beam radius
    """
    return W0 * (Theta0 ** 2 + Lambda0 ** 2) ** (1 / 2)


def Theta0(z, F0):
    """

    :param z: Distance to transmitter
    :param F0: Phase front radius of curvature
    :return:
    """
    return 1 - z / F0


def Lambda0(z, k, W0):
    """

    :param z: Distance to transmitter
    :param k: Wavenumber
    :param W0: Beam radius
    :return:
    """
    return 2 * z / (k * W0 ** 2)


def mu2d(hh: np.ndarray, C_n2: np.ndarray) -> float:
    yy = [C_n2[i] * ((h - hh[0]) / (hh[-1] - h[0])) ** (5 / 3) for i, h in enumerate(hh)]
    integral = integrate.simpson(yy, hh)
    return integral


def Lambda(Theta0, Lambda0):
    """

    :param Theta0:
    :param Lambda0:
    :return:
    """
    return Lambda0 / (Theta0 ** 2 + Lambda0 ** 2)


def F0(W0, z, wavelambda):
    """

    :param W0: Beam waist radius
    :param z: Distance along the transmitting path
    :param wavelambda: Wavelength
    :return: Phase front radius of curvature
    """
    return z * (1 + (math.pi * W0 ** 2 / (wavelambda * z)) ** 2)


def main():
    with open('../Data/DFs/Cn.pickle', 'rb') as f:
        Cn = pickle.load(f)

    zz = np.array(Cn['z-distance'])
    C_n2 = np.array(Cn['Cn^2'])
    hh = np.array(Cn['altitude'])

    W0 = None
    wavelambda = 1550
    k = 2 * math.pi / wavelambda
    H = 900
    h0 = 600
    F0 = F0(W0, z, wavelambda)
    lambda0 = Lambda0(z, k, W0)
    Theta0 = Theta0(z, F0)
    Lambda = Lambda(Theta0, Lambda0)
    mu_2d = mu2d(C_n2, hh)
    W = W(W0, Theta0, Lambda0)
    WLT = WLT(W, mu2d, Lambda, k, H, h0)
    I0 = IO(W0, WLT)


if __name__ == '__main__':
    main()
