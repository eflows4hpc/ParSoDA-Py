import emoji

from parsoda import SocialDataItem
from parsoda.model import Filter


class HasTags(Filter):

    def test(self, item: SocialDataItem):
        return item.has_tags()
