from abc import ABC

from parsoda import SocialDataItem
from parsoda.model import Filter


class IsGeotagged(Filter):
    """
    Questa classe permette di verificare se un abstract_geotagged_item ha informazioni
    relative alla geolocalizzazione
    """

    def test(self, item: SocialDataItem):
        return item.has_location()
