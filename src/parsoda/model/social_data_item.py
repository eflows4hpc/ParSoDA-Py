from datetime import datetime
from typing import Optional, List, Dict

from parsoda.utils.json_serializer import obj_to_json, obj_from_json


class ItemPostTime:
    year: int = None
    month: int = None
    day: int = None
    hour: int = None
    minute: int = None
    second: int = None

    def __init__(self, other: datetime):
        self.year = other.year
        self.month = other.month
        self.day = other.day
        self.hour = other.hour
        self.minute = other.minute
        self.second = other.second

    def to_datetime(self) -> datetime:
        return datetime(
            self.year,
            self.month,
            self.day,
            self.hour,
            self.minute,
            self.second
        )

    def __eq__(self, other) -> bool:
        return \
            self.year == other.year and \
            self.month == other.month and \
            self.day == other.day and \
            self.hour == other.hour and \
            self.minute == other.minute and \
            self.second == other.second


class ItemLocation:
    latitude: float
    longitude: float

    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

    def __eq__(self, other) -> bool:
        return \
            self.latitude == other.latitude and \
            self.longitude == other.longitude


class SocialDataItem:
    
    def __init__(self):
        self.id = ''
        self.user_id: str = ''
        self.user_name: str = ''
        self.text: str = ''
        self.tags: List = []
        self.extras: Dict = {}
        self.date_posted: Optional[ItemPostTime] = ItemPostTime(datetime(1, 1, 1))
        self.location: Optional[ItemLocation] = None

        self.original_format: str = '<unknown>'

    def has_user_id(self):
        return self.user_id is not None and self.user_id != ''

    def has_user_name(self):
        return self.user_name is not None and self.user_name != ''

    def has_text(self):
        return self.text is not None and self.text != ''

    def has_tags(self) -> bool:
        return len(self.tags) > 0

    def has_extras(self) -> bool:
        return len(self.extras) > 0

    def has_date_posted(self) -> bool:
        return self.date_posted is not None

    def has_location(self) -> bool:
        return self.location is not None

    def to_json(self) -> str:
        return obj_to_json(self)

    def from_json(self, json_string: str):
        self.__dict__ = obj_from_json(json_string).__dict__
        return self
        
    def __key(self):
        return (self.id, self.user_id, self.user_name)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other) -> bool:
        return self.id == other.id \
               and self.user_id == other.user_id \
               and self.user_name == other.user_name \
               and self.date_posted == other.date_posted \
               and self.text == other.text \
               and self.tags == other.tags \
               and self.location == other.location \
               and self.extras == other.extras

    def __str__(self) -> str:
        return self.to_json()

    def __repr__(self) -> str:
        return self.to_json()


class SocialDataItemBuilder:

    def __init__(self):
        self.item = SocialDataItem()

    def build(self) -> SocialDataItem:
        """
        Build the SocialDataItem.
        After invoking this method, the builder is no longer usable.
        :return: a new SocialDataItem
        """
        built = self.item
        self.item = None
        return built

    def set_id(self, id: str):
        self.item.id = str(id)
        return self

    def set_user_id(self, user_id: str):
        self.item.user_id = str(user_id)
        return self

    def set_user_name(self, user_name: str):
        self.item.user_name = str(user_name)
        return self

    def set_date_posted(self, date_posted: datetime):
        self.item.date_posted = ItemPostTime(date_posted)
        return self

    def set_text(self, text: str):
        self.item.text = str(text)
        return self

    def set_tags(self, tags: List):
        self.item.tags = tags
        return self

    def set_location(self, latitude: float, longitude: float):
        self.item.location = ItemLocation(latitude, longitude)
        return self

    def put_extra(self, key, value):
        self.item.extras[key] = value
        return self

    def del_extra(self, key):
        del self.item.extras[key]
        return self

    def clear_extras(self):
        self.item.extras.clear()
        return self

    def set_extras(self, extras: dict):
        """
        Sets all extras at once from a standard dictionary.
        Invoking this method all the extras previously set are deleted.
        :param extras: dictionary
        :return:
        """
        self.item.extras = {}
        for key in extras:
            self.item.extras[key] = extras[key]
        return self

    def set_original_format(self, original_format: str):
        self.item.original_format = original_format
        return self
