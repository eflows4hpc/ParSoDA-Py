from abc import ABC
from typing import Generic, TypeVar, List

K = TypeVar('K')
V = TypeVar('V')
R = TypeVar('R')


class Reducer(ABC, Generic[K, V, R]):
    """
    Defines a ParSoDA Reducer
    """

    def reduce(self, key: K, values: List[V]) -> R:
        """Applies the reduction algorithm to values

        Args:
            key (K): the key all values are associated to
            values (List[V]): all the values associated to the key

        Returns:
            R: the reduced value
        """
        pass