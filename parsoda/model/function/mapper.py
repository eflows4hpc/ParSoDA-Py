from abc import ABC, abstractmethod
from typing import Generic, Iterable, TypeVar, Tuple

from parsoda.model.social_data_item import SocialDataItem

K = TypeVar('K')
V = TypeVar('V')


class Mapper(ABC, Generic[K, V]):
    """
    Defines a ParSoDA Mapper
    """

    @abstractmethod
    def map(self, item: SocialDataItem) -> Iterable[Tuple[K, V]]:
        """Returns a list of key-value pairs computed from the given item.
        Example result: [ (item.user_id, item.tags[0]), (item.user_id, item.tags[1]), ... ]

        Args:
            item (SocialDataItem): the item to map

        Returns:
            Iterable[Tuple[K, V]]: an iterable of key-value pairs
        """
        pass
