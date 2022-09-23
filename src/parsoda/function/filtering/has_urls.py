from typing import Optional

import emoji

from parsoda import SocialDataItem
from parsoda.model import Filter
import re


class HasUrls(Filter):
    """
    Retains only the items that contains one of the specified URLs.
    If no URL is specified, it retains only the items that contains at least one URL.
    """

    _url_regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s(" \
                 r")<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’])) "

    def __init__(self, urls: Optional[list[str]] = None, separator: str = ","):
        self.urls = urls
        self.separator = separator

    def test(self, item: SocialDataItem):
        # extract URLs from item text
        urls = re.findall(HasUrls._url_regex, item.text)

        if self.urls is not None:
            # return true if at least one of the specified URLs is in the item
            for url in self.urls:
                if url in urls:
                    return True
        else:
            # return true if the item contains at least one URL
            return len(urls) > 0
