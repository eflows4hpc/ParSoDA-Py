import json
from datetime import datetime

from parsoda import SocialDataItem
from parsoda.model import Parser

from parsoda.model.social_data_item import SocialDataItemBuilder


class ParsodaParser(Parser):

    def __call__(self, text_line):
        try:
            return SocialDataItem.from_json(text_line)
        except Exception as e:
            print(e)
            return None