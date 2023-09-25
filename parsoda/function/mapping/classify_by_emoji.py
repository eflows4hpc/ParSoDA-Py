# -*- coding: utf-8 -*-
from typing import List, Tuple

from parsoda import SocialDataItem
from parsoda.model import Mapper
from parsoda.utils.emoji_utils import get_emojis, load_emojis


class ClassifyByEmoji(Mapper[str, int]):
    """
    SocialDataItem -> (user_id, sum_polarity)

    Maps a social data item to a key-value pair,
    where key is the user id of the item and value is
    the sum of the polarities of all emojis found in the text
    of the item.
    """

    def __init__(self, emoji_path: str):
        self.emojis = load_emojis(emoji_path)

    def map(self, item: SocialDataItem) -> List[Tuple[str, int]]:
        sum_polarity = 0

        # prendiamo le emoji del post
        item_emojis = get_emojis(item.text)
        
        # for e, p in self.emojis

        # calcoliamo la polarità in base alle emoji
        for emo in item_emojis:
            if emo in self.emojis:
                sum_polarity += self.emojis[emo]

        return [(item.user_id, sum_polarity)]
