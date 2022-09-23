from typing import Optional, List

from parsoda.model import Reducer


class ReduceByEmojiPolarity(Reducer[str, int, Optional[int]]):

    def __init__(self, min_polarity_threshold: int = 1):
        self.min_polarity_threshold = min_polarity_threshold

    def reduce(self, key: str, polarities: List[int]) -> Optional[int]:
        polarity_sum = sum(polarities)

        # filter by threshold
        if polarity_sum >= self.min_polarity_threshold:
            return polarity_sum
        else:
            return None

