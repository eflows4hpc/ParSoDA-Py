# coding=utf-8
import shapely.geometry
from shapely.geometry import Point

from shapely.geometry import shape
from parsoda import SocialDataItem
from parsoda.model import Filter


class IsInShape(Filter):
    """
    Tests if an item is in the given geometrical shape
    """

    def __init__(self, shape: shape):
        self.shape = shape

    def test(self, item: SocialDataItem):
        if not item.has_location():
            return False
        location = Point(item.location.latitude, item.location.longitude)
        return location.within(self.shape)
