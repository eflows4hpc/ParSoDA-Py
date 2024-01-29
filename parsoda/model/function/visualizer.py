from abc import abstractmethod, ABC
from typing import TypeVar, Generic

A = TypeVar('A')


class Visualizer(ABC, Generic[A]):
    """
    Defines a ParSoDA Visualizer
    """

    @abstractmethod
    def visualize(self, result: A) -> None:
        """Transforms data from the analysis step in some output format, then write them to some output device or system.

        Args:
            result (A): the data resulting from the analysis step
        """
        pass
