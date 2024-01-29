from abc import ABC, abstractmethod

from parsoda.model.social_data_item import SocialDataItem


class Filter(ABC):
    """
    Defines a ParSoDA Filter
    """

    @abstractmethod
    def test(self, item: SocialDataItem) -> bool:
        """Test if the item satisfies the predicate of the filter

        Args:
            item (SocialDataItem): the item to test

        Returns:
            bool: True if the item satisfies the predicate, False otherwise
        """        
        pass