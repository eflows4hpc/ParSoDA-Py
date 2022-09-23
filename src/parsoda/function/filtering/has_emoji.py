import unicodedata
import emoji

from parsoda import SocialDataItem
from parsoda.model import Filter


class HasEmoji(Filter):
    """
    Questa classe permette di verificare se un abstract_geotagged_item contiene un emoji in qualche campo
    (considerando tutto il json da cui è ricavato l'abstract_geotagged_item)
    """

    def test(self, item: SocialDataItem):
        for language, emojis in emoji.unicode_codes.UNICODE_EMOJI.items():
            for e in emojis:
                if item.text.find(e) >= 0:
                    #print(f"emoji found {e}")
                    return True
        return False
