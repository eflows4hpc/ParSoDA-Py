from abc import abstractmethod, ABC
from typing import TypeVar, Generic

A = TypeVar('A')


class Visualizer(ABC, Generic[A]):
    """
    Defines a ParSoDA Visualizer
    """

    @abstractmethod
    def visualize(self, result: A) -> None:
        pass
