from __future__ import annotations

import pickle

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy import integrate

from combined_fit.indices import rytov_index, scintillation_index
from formula.jitter import k
from formula.normalize import norm_I


def integrate_scint_index(I: np.ndarray, ii: np.ndarray | float):
    return np.array([integrate.quad(lambda I_0: calc_probs(I, i, I_0), 0, 1)[0] for i in ii])


def calc_probs(I: np.ndarray, ii: np.ndarray | float, I_0: float = None) -> np.ndarray:
    Cn = pd.read_pickle('Data/DFs/Cn.pickle')

    zz = np.array(Cn['z-distance'])
    C_n2 = np.array(Cn['Cn^2'])

    labda = 1e-6  # Wavelength (unknown)

    sigma_R2 = rytov_index(k(labda), zz, C_n2)
    sigma_I2 = scintillation_index(sigma_R2)

    I_0 = norm_I(I).mean() if not I_0 else I_0
    I_0 = 0.02
    return probability_dist(ii, I_0, sigma_I2)  # return array


def probability_dist(I: float | np.ndarray, I_0: float, sigma_I2: float) -> float | np.ndarray:
    return 1 / (I * sigma_I2 * np.sqrt(2 * np.pi)) * np.exp(
        - (np.log(I / I_0) + 0 + sigma_I2 / 2) ** 2 / (2 * sigma_I2)
    )


if __name__ == '__main__':
    with open('../Data/DFs/data11/off1.pickle', 'rb') as f:
        data = pickle.load(f)
    I = np.array(data)
    ii = np.linspace(0, 1, 101)[1:]
    p_sc = integrate_scint_index(I, ii)
    plt.plot(ii, p_sc)
    plt.show()
