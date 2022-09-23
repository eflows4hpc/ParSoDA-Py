# coding=utf-8
from shapely.geometry import Point

from parsoda.utils.roi import load_RoIs
from parsoda import SocialDataItem
from parsoda.model import Filter


class IsInRoI(Filter):
    """
    Questa classe permette di verificare se un abstract_geotagged_item che ha informazioni
    relative alla geolocalizzazione, è geotaggato in almeno uno delle RoI passate al costruttore
    """

    def __init__(self, path_rois: str):
        self.rois = load_RoIs(path_rois)

    def test(self, item: SocialDataItem):
        if not item.has_location():
            return False
        location = Point(item.location.latitude, item.location.longitude)
        for roi in self.rois:
            if location.within(roi.shape):
                return True
        return False
