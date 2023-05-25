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
        pass