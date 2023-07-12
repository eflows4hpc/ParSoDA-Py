# coding=utf-8
import datetime

from datetime import datetime

from parsoda.utils.roi import load_RoIs
from parsoda import SocialDataItem
from parsoda.model import Filter


class IsInDate(Filter):

    def __init__(self, start: datetime, end: datetime):
        self.start = start
        self.end = end

    def test(self, item: SocialDataItem):
        if item.has_date_posted():
            item_time = item.date_posted.to_datetime()
            return self.start < item_time < self.end
        return False
