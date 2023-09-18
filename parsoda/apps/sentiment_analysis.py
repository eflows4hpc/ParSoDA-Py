from typing import List

from parsoda import SocialDataApp
from parsoda.function.analysis.gap_bide_analysis import GapBIDE
from parsoda.function.filtering import IsInRoI

from parsoda.function.mapping.find_poi import FindPoI
from parsoda.function.reduction.reduce_by_trajectories import ReduceByTrajectories
from parsoda.function.visualization.sort_gap_bide import SortGapBIDE
from parsoda.model.driver.parsoda_driver import ParsodaDriver
from parsoda.model.function.crawler import Crawler


def parsoda_sentiment_analysis(
    driver: ParsodaDriver,
    crawlers: List[Crawler],
    rois_file: str,
    *, 
    num_partitions=-1, 
    chunk_size=64,
    emoji_file="./resources/input/emoji.json", 
    visualization_file="./resources/output/emoji_polarization.txt",
):  
    app = SocialDataApp("Trajectory Mining", driver, num_partitions=num_partitions, chunk_size=chunk_size)
    app.set_crawlers(crawlers)
    app.set_filters([
        HasEmoji()
    ])
    app.set_mapper(ClassifyByEmoji(emoji_file))
    app.set_reducer(ReduceByEmojiPolarity())
    app.set_analyzer(TwoFactionsPolarization())
    app.set_visualizer(PrintEmojiPolarization(visualization_file))
    return app
