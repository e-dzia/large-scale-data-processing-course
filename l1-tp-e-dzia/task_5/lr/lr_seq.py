"""Basic linear regression."""
from typing import List

from l1.task_5.lr import base


class LinearRegressionSequential(base.LinearRegression):
    """Basic linear regression."""

    def fit(self, X: List[float], y: List[float]) -> base.LinearRegression:
        """Fit function."""
        self._coef = [0, 0]

        n = len(X)
        m_x, m_y = sum(X) / n, sum(y) / n

        SS_xy = 0
        SS_xx = 0
        for x_element, y_element in zip(X, y):
            SS_xy += (x_element - m_x) * (y_element - m_y)
            SS_xx += (x_element - m_x) ** 2

        self._coef[1] = SS_xy / SS_xx
        self._coef[0] = m_y - self._coef[1] * m_x

        return self
