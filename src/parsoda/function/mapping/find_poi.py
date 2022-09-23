# coding=utf-8
from datetime import datetime
from typing import List, Tuple, Optional

from shapely.geometry import Point

from parsoda import SocialDataItem
from parsoda.model import Mapper
from parsoda.utils.roi import RoI, load_RoIs

"""
    Questa classe effettua un mapping usando informazioni
    relative alla geolocalizzazione
    
    ritorna una tupla: (userId, (dateTime_post, RoI_post))
    con RoI_post la RoI più piccola in cui ricade il post
"""


class FindPoI(Mapper[str, Tuple[datetime, RoI]]):

    def __init__(self, rois_path: str):
        self.rois = load_RoIs(rois_path)

    def map(self, item: SocialDataItem) -> List[Tuple[str, Tuple[datetime, RoI]]]:
        if not item.has_location():
            return []

        location = item.location

        tmp_roi: Optional[RoI] = None
        for roi in self.rois:
            point = Point(location.latitude, location.longitude)
            if point.within(roi.shape):
                if (tmp_roi is None) or (tmp_roi.get_area_squared_km() > roi.get_area_squared_km()):
                    tmp_roi = roi

        return [(item.user_id, (item.date_posted.to_datetime(), tmp_roi))]
