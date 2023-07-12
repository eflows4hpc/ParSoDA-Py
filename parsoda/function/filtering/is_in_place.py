from abc import ABC

from geopy.distance import geodesic

from parsoda import SocialDataItem
from parsoda.model import Filter


class IsInPlace(Filter):
    """
    Questa classe permette di verificare che un abstract_geotagged_item sia
    geolocalizzato all'interno della zona (circolare) ricavata dai parametri in
    input al costruttore (command_options)
    """

    def __init__(self, latitude: float, longitude: float, radius: float):
        self.lat = latitude
        self.lng = longitude
        self.radius = radius

    def test(self, item: SocialDataItem):
        if item.has_location():
            lat = item.location.latitude
            lng = item.location.longitude
            distance = geodesic((lat, lng), (self.lat, self.lng), ellipsoid='WGS-84').m
            return distance <= self.radius
        return False
