from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Dict

from parsoda.model.driver.parsoda_driver import ParsodaDriver

K = TypeVar('K')  # key type
R = TypeVar('R')  # reducer output type
A = TypeVar('A')  # analysis output type


class Analyzer(ABC, Generic[K, R, A]):
    """
    Defines a ParSoDA Analyzer
    """

    @abstractmethod
    def analyze(self, driver: ParsodaDriver, data: Dict[K, R]) -> A:
        """Applies an analysis algorithm to the output data from reduction step.
        The analyzer might be a sequential, parallel or distributed algorithm.
        In the latter case, the algorithm would use the same driver used by the current application for running a new, nested, ParSoDA application.

        Args:
            driver (ParsodaDriver): the driver used during the execution of the parallel phase
            data (Dict[K, R]): output data from reducton step organized as a dictionary of key-value pairs

        Returns:
            A: the outputdata type from the analysis
        """
        pass