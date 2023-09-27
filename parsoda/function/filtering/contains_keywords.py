from parsoda import SocialDataItem
from parsoda.model import Filter


class ContainsKeywords(Filter):
    """
    Checks if an item contains at least the specified number (threshold) of the given keywords
    """    
    
    def __init__(self, keywords, separator=' ', threshold: int = 1):
        """Define a filter for items which include keywords

        Args:
            keywords (_type_): The keywords that must be included in items as a single string
            separator (str, optional): the separator of the keywords in the specified string. Defaults to ' ' (space).
            threshold (int, optional): The number of different keywords that must be included in the item text. Defaults to 1.
        """        
        self.__keywords = keywords.split(separator)
        self.__threshold = threshold

    def test(self, item: SocialDataItem):
        if self.__keywords is None or self.__keywords == "":
            return True
        contains = 0
        for keyword in self.__keywords:
            if keyword in item.text:
                contains+=1
                if contains >= self.__threshold:
                    return True
        return False
