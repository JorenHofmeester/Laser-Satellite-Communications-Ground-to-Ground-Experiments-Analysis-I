from dataclasses import dataclass, field

import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import beta

from formula.normalize import norm_I


@dataclass
class IntensityDistribution:
    intensities: np.ndarray
    w_0: float = field(default=16e-6 / np.pi * 180)
    a: float = 1

    @property
    def norm_I(self) -> np.ndarray:
        return (norm_I(self.intensities) + 1e-10) / (1 + 1e-8)  # weird stuff to make 0 < norm_I < 1

    def fit(self) -> list:
        return beta.fit(self.norm_I, fa=1, floc=0, fscale=1)

    @property
    def sigma(self) -> float:
        beta1 = self.b
        sigma1 = np.sqrt(self.w_0 ** 2 / (4 * beta1))
        return sigma1

    # @property
    # def a(self) -> float:
    #     return self.fit()[0]

    @property
    def b(self) -> float:
        return self.fit()[1]

    def plot(self):
        plt.hist(self.norm_I, bins=101, density=True, label='data')
        # I = np.linspace(beta.ppf(0.01, self.a, self.b), beta.ppf(0.99, self.a, self.b), 101)
        I = np.linspace(0, 1, 101)
        plt.plot(I, beta.pdf(I, self.a, self.b), 'r-', label='beta pdf')
        plt.ylim(0, 10)
        plt.legend()
