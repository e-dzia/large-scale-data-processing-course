"""Base classes."""

import abc
from typing import List

import numpy as np


class ScikitPredictor(abc.ABC):
    """Predictor base class."""

    @abc.abstractmethod
    def fit(self, X, y):
        """Fit function."""
        pass

    @abc.abstractmethod
    def predict(self, X):
        """Predict function."""
        pass


class LinearRegression(ScikitPredictor):
    """Linear Regression base class."""

    def __init__(self):
        """Linear Regression init."""
        self._coef = None
        self.alpha = 0.05

    @abc.abstractmethod
    def fit(self, X: List[float], y: List[float]) -> "LinearRegression":
        """Fit function."""
        pass

    def predict(self, X: List[float]) -> np.ndarray:
        """Predict function."""
        if self._coef is None:
            raise RuntimeError('Please fit model before prediction')

        return self._coef[0] + self._coef[1] * np.array(X)
