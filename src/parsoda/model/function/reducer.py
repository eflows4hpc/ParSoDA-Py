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
        """
        Applies the reduction algorithm to values
        :param key: the key all values are associated to
        :param values: all the values associated to the key
        :return: the reduced value
        """
        pass