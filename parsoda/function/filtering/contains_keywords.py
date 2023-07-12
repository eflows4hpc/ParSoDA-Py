from parsoda import SocialDataItem
from parsoda.model import Filter


class ContainsKeywords(Filter):
    """
    Checks if an item contains at least one of the given keywords
    """

    def __init__(self, keywords, separator=':'):
        self.keywords = keywords.split(separator)

    def test(self, item: SocialDataItem):
        for keyword in self.keywords:
            if keyword in item.text:
                return True
        return False
