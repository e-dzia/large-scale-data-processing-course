"""Linear Regression using multiprocessing."""
import math
import os
from concurrent.futures import ProcessPoolExecutor
from typing import List

from l1.task_5.lr import base


class LinearRegressionProcess(base.LinearRegression):
    """Linear Regression using multiprocessing."""

    def fit(self, X: List[float], y: List[float]) -> base.LinearRegression:
        """Fit function."""
        self._coef = [0, 0]

        n = len(X)
        num_threads = self._get_threads_number()
        executor = ProcessPoolExecutor(num_threads)

        m_x, m_y = sum(X) / n, sum(y) / n

        batches_x = self.batch_data(X, num_threads)
        batches_y = self.batch_data(y, num_threads)

        coefficients = []
        for i in range(num_threads):
            coef = executor.submit(self.count_SS, batches_x[i],
                                   batches_y[i], m_x, m_y)
            coefficients.append(coef)

        SS_xy, SS_xx = 0, 0
        for coef in coefficients:
            SS_xy_batch, SS_xx_batch = coef.result()
            SS_xy += SS_xy_batch
            SS_xx += SS_xx_batch

        self._coef[1] = SS_xy / SS_xx
        self._coef[0] = m_y - self._coef[1] * m_x

        return self

    def count_SS(self, X, y, m_x, m_y):
        """Counting variance and covariance."""
        SS_xy = 0
        SS_xx = 0
        for x_element, y_element in zip(X, y):
            SS_xy += (x_element - m_x) * (y_element - m_y)
            SS_xx += (x_element - m_x) ** 2
        return SS_xy, SS_xx

    @staticmethod
    def batch_data(x, num_batches):
        """Dividing data into batches."""
        n = len(x)
        batch_size = math.ceil(n / num_batches)
        batches = []
        for i in range(num_batches):
            batches.append(x[int(i * batch_size): int((i + 1) * batch_size)])
        return batches

    @staticmethod
    def _get_threads_number():
        """Returns number of threads."""
        return os.cpu_count()  # there is no method to get phisical CPU cores :(
