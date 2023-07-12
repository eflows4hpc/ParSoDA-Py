# -*- coding: utf-8 -*-
from typing import List, Tuple

from parsoda import SocialDataItem
from parsoda.model import Mapper
from parsoda.utils.emoji_utils import get_emojis, load_emojis


class ClassifyByGeocell(Mapper[Tuple[float, float], SocialDataItem]):
    """
    item -> ((lat,lon), item)
    """

    # static variables
    step1mY: float = 8.992909382672273E-6
    step1mX: float = 1.2080663828690774E-5

    def __init__(self, x_step: float = 0, y_step: float = 0):
        self.x_step = x_step
        self.y_step = y_step

    def map(self, item: SocialDataItem) -> List[Tuple[Tuple[float, float], SocialDataItem]]:
        if item.has_location():
            lat, lon = self.calculate_cell_coords(item.location.latitude, item.location.longitude)
            cell = (lat, lon)
            return [(cell, item)]
        else:
            return []

    def calculate_cell_coords(self, latitude: float, longitude: float) -> Tuple[float, float]:
        step_y = self.step1mY * self.y_step
        step_x = self.step1mX * self.x_step
        lat = ((latitude/step_y)+1)*step_y
        lon = ((longitude/step_x)+1)*step_x
        return lat, lon
