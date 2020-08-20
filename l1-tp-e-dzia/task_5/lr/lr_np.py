"""Linear Regression implemented using numpy."""

from typing import List
import numpy as np

from l1.task_5.lr import base


class LinearRegressionNumpy(base.LinearRegression):
    """Linear Regression implemented using numpy."""

    def fit(self, X: List[float], y: List[float]) -> base.LinearRegression:
        """Fit function."""
        self._coef = [0, 0]
        X = np.array(X)
        y = np.array(y)

        n = np.size(X)
        m_x, m_y = np.mean(X), np.mean(y)

        # calculating cross-deviation and deviation about x
        SS_xy = np.sum(y * X) - n * m_y * m_x
        SS_xx = np.sum(X * X) - n * m_x * m_x

        self._coef[1] = SS_xy / SS_xx
        self._coef[0] = m_y - self._coef[1] * m_x

        return self
