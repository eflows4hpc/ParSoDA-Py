from datetime import datetime
import json
from typing import Optional, List, Dict, final

from parsoda.utils.json_serializer import obj_to_json, obj_from_json


@final
class ItemPostTime:
    """
    Class used for representing the time of posts
    """
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
        """Convert the object to a standard datetime object

        Returns:
            datetime: the datetime object built
        """
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
            
    def to_json(self) -> str:
        """Serialize the item to JSON.

        Returns:
            str: JSON representation of this item
        """
        json_dict = {}
        json_dict["timestamp"] = self.to_datetime().timestamp()
        return json.dumps(json_dict)
    
    @staticmethod
    def from_json(json_str: str):
        """Deserialize a social data item from JSON.

        Returns:
            SocialDataItem: the deserialized data item
        """
        timestamp = int(json.loads(json_str)['timestamp'])
        dt = datetime.fromtimestamp(timestamp)
        return ItemPostTime(dt)


@final
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


@final
class SocialDataItem:
    """Class for defining ParSoDA-Py's standard representantion of social data items.
    An instance of this class can be serialized as a JSON
    """
    
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
        """Check if this item has a user ID.

        Returns:
            Boolean: true if the items has a user ID, false otherwise
        """
        return self.user_id is not None and self.user_id != ''

    def has_user_name(self):
        """Check if this item has a user name.

        Returns:
            Boolean: true if the items has a user name, false otherwise
        """
        return self.user_name is not None and self.user_name != ''

    def has_text(self):
        """Check if this item has text.

        Returns:
            Boolean: true if the items has text, false otherwise
        """
        return self.text is not None and self.text != ''

    def has_tags(self) -> bool:
        """Check if this item has tags.

        Returns:
            Boolean: true if the items has tags, false otherwise
        """
        return len(self.tags) > 0

    def has_extras(self) -> bool:
        """Check if this item has extra data.

        Returns:
            Boolean: true if the items has extra data, false otherwise.
        """
        return len(self.extras) > 0

    def has_date_posted(self) -> bool:
        """Check if this item has posting date.

        Returns:
            Boolean: true if the items has posting date, false otherwise.
        """
        return self.date_posted is not None

    def has_location(self) -> bool:
        """Check if this item has a location.

        Returns:
            Boolean: true if the items has a location, false otherwise
        """
        return self.location is not None

    def to_json(self) -> str:
        """Serialize the item to JSON.

        Returns:
            str: JSON representation of this item
        """
        json_dict = {}
        json_dict['id'] = self.id
        json_dict['user_id'] = self.user_id
        json_dict['user_name'] = self.user_name
        json_dict['text'] = self.text
        json_dict['tags'] = self.tags
        json_dict['original_format'] = self.original_format
        json_dict['extras'] = obj_to_json(self.extras)
        json_dict['date_posted'] = self.date_posted.to_datetime().timestamp() if self.date_posted is not None else "None"
        json_dict['location'] = (self.location.latitude, self.location.longitude) if self.location is not None else "None"
        return json.dumps(json_dict)
        
        #return obj_to_json(self)

    @staticmethod
    def from_json(json_string: str):
        """Deserialize a social data item from JSON.

        Returns:
            SocialDataItem: the deserialized data item
        """
        self = SocialDataItem()
        json_dict = json.loads(json_string)
        
        self.id = json_dict['id']
        self.user_id = json_dict['user_id']
        self.user_name = json_dict['user_name']
        self.text = json_dict['text']
        self.tags = json_dict['tags']
        self.original_format = json_dict['original_format']
        self.extras = obj_from_json(json_dict['extras'])
        self.date_posted = ItemPostTime(datetime.fromtimestamp(json_dict['date_posted'])) if json_dict['date_posted'] != "None" else None
        self.location = ItemLocation(json_dict['location'][0], json_dict['location'][1]) if json_dict['location'] != "None" else None
        
        #self.__dict__ = obj_from_json(json_string).__dict__
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
    """Class used for building new social data items
    """

    def __init__(self):
        self.item = SocialDataItem()

    def build(self) -> SocialDataItem:
        """
        Build the SocialDataItem.
        After invoking this method, the builder is no longer usable.
        :return: a new SocialDataItem
        """
        built = self.item
        self.item = SocialDataItem()
        return built

    def set_id(self, id: str):
        """Sets the item ID

        Args:
            id (str): the item ID

        Returns:
            SocialDataItemBuilder: this builder
        """
        self.item.id = str(id)
        return self

    def set_user_id(self, user_id: str):
        """Sets the user ID

        Args:
            id (str): the user ID

        Returns:
            SocialDataItemBuilder: this builder
        """
        self.item.user_id = str(user_id)
        return self

    def set_user_name(self, user_name: str):
        """Sets the user name.

        Args:
            user_name (str): the user name.

        Returns:
            SocialDataItemBuilder: this builder
        """
        self.item.user_name = str(user_name)
        return self

    def set_date_posted(self, date_posted: datetime):
        """Sets the posting date.

        Args:
            id (str): the posting date

        Returns:
            SocialDataItemBuilder: this builder
        """
        self.item.date_posted = ItemPostTime(date_posted)
        return self

    def set_text(self, text: str):
        """Sets the item text.

        Args:
            id (str): the item text

        Returns:
            SocialDataItemBuilder: this builder
        """
        self.item.text = str(text)
        return self

    def set_tags(self, tags: List):
        """Sets the list of tags

        Args:
            id (str): the list of tags

        Returns:
            SocialDataItemBuilder: this builder
        """
        self.item.tags = tags
        return self

    def set_location(self, latitude: float, longitude: float):
        """Sets the item location.

        Args:
            id (str): the item location

        Returns:
            SocialDataItemBuilder: this builder
        """
        self.item.location = ItemLocation(latitude, longitude)
        return self

    def put_extra(self, key, value):
        """Add extra data to the item

        Args:
            key (str): the data key
            value: the value data

        Returns:
            SocialDataItemBuilder: this builder
        """
        self.item.extras[key] = value
        return self

    def del_extra(self, key):
        """Delete an extra value.

        Args:
            key (str): the key of the data value to remove

        Returns:
            SocialDataItemBuilder: this builder
        """
        del self.item.extras[key]
        return self

    def clear_extras(self):
        """Clears the extra data

        Returns:
            SocialDataItemBuilder: this builder
        """
        self.item.extras.clear()
        return self

    def set_extras(self, extras: dict):
        """
        Sets all extras at once from a standard dictionary.
        Invoking this method all the extras previously set are deleted.

        Args:
            extras (str): the extra dictionary

        Returns:
            SocialDataItemBuilder: this builder
        """
        self.item.extras = {}
        for key in extras:
            self.item.extras[key] = extras[key]
        return self

    def set_original_format(self, original_format: str):
        """Sets a name for the item original format

        Args:
            original_format (str): a name for the original format

        Returns:
            SocialDataItemBuilder: this builder
        """
        self.item.original_format = original_format
        return self
