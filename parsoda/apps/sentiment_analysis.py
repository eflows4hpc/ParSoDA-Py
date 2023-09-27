from typing import List

from parsoda import SocialDataApp
from parsoda.function.analysis.gap_bide_analysis import GapBIDE
from parsoda.function.filtering import HasEmoji
from parsoda.function.filtering.contains_keywords import ContainsKeywords

from parsoda.function.mapping.classify_by_emoji import ClassifyByEmoji
from parsoda.function.reduction.reduce_by_emoji_polarity import ReduceByEmojiPolarity
from parsoda.function.analysis.two_factions_polarization import TwoFactionsPolarization
from parsoda.function.visualization.print_emoji_polarization import PrintEmojiPolarization
from parsoda.model.driver.parsoda_driver import ParsodaDriver
from parsoda.model.function.crawler import Crawler


def parsoda_sentiment_analysis(
    driver: ParsodaDriver,
    crawlers: List[Crawler],
    *, 
    num_partitions=-1, 
    chunk_size=64,
    emoji_file="./resources/input/emoji.json", 
    visualization_file="./resources/output/emoji_polarization.txt",
    keywords: str = "",
    keywords_separator: str = " ",
    keywords_threshold: int = 1
):  
    app = SocialDataApp("Sentiment Analysis", driver, num_partitions=num_partitions, chunk_size=chunk_size)
    app.set_crawlers(crawlers)
    app.set_filters([
        ContainsKeywords(
            keywords=keywords, 
            separator=keywords_separator, 
            threshold=keywords_threshold
        ),
        HasEmoji()
    ])
    app.set_mapper(ClassifyByEmoji(emoji_file))
    app.set_reducer(ReduceByEmojiPolarity())
    app.set_analyzer(TwoFactionsPolarization())
    app.set_visualizer(PrintEmojiPolarization(visualization_file))
    return app
