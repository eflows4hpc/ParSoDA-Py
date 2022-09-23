import emoji

from parsoda import SocialDataItem
from parsoda.model import Filter


class HasLang(Filter):

    def __init__(self, lang: str):
        self.lang = lang

    def test(self, item: SocialDataItem):
        return item.extras['lang'] == self.lang
