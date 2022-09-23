import argparse
from datetime import date

from pyspark import SparkContext, SparkConf

from parsoda import SocialDataApp
from parsoda.function.analysis.gap_bide_analysis import GapBIDE
from parsoda.function.analysis.two_factions_polarization import TwoFactionsPolarization
from parsoda.function.crawling.local_file_crawler import LocalFileCrawler
from parsoda.function.crawling.parsing.flickr_parser import FlickrParser
from parsoda.function.crawling.parsing.twitter_parser import TwitterParser
from parsoda.function.crawling.parsing.vinitaly2019_parser import Vinitaly2019Parser
from parsoda.function.filtering import IsGeotagged, IsInPlace, IsInRoI, HasEmoji
import sys

from parsoda.function.mapping.classify_by_emoji import ClassifyByEmoji
from parsoda.function.mapping.find_poi import FindPoI
from parsoda.function.reduction.reduce_by_emoji_polarity import ReduceByEmojiPolarity
from parsoda.function.reduction.reduce_by_trajectories import ReduceByTrajectories
from parsoda.function.visualization.print_emoji_polarization import PrintEmojiPolarization
from parsoda.function.visualization.sort_gap_bide import SortGapBIDE
from parsoda.model.driver.parsoda_multicore_driver import ParsodaMultiCoreDriver
from parsoda.model.driver.parsoda_pycompss_driver import ParsodaPyCompssDriver
from parsoda.model.driver.parsoda_pyspark_driver import ParsodaPySparkDriver
from parsoda.model.driver.parsoda_singlecore_driver import ParsodaSingleCoreDriver
from parsoda.utils.roi import RoI

def parse_command_line():
    parser = argparse.ArgumentParser(description='Emoji Polarization')
    parser.add_argument("partitions",
                        type=int,
                        default=8,
                        help="specifies the number of data partitions.")
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_command_line()

    driver = ParsodaPyCompssDriver()
    
    app = SocialDataApp("Emoji Polarization", driver, num_partitions=args.partitions)

    app.set_crawlers([
        LocalFileCrawler('./resources/input/TwitterRome2017_100k.json', TwitterParser()),
        LocalFileCrawler('./resources/input/flickr100k.json', FlickrParser()),
        LocalFileCrawler('./resources/input/vinitaly2019.json', Vinitaly2019Parser()),
    ])
    app.set_filters([
        HasEmoji()
    ])
    app.set_mapper(ClassifyByEmoji("./resources/input/emoji.json"))
    app.set_reducer(ReduceByEmojiPolarity())
    app.set_analyzer(TwoFactionsPolarization())
    app.set_visualizer(PrintEmojiPolarization('./resources/output/emoji_polarization.txt'))

    app.execute()
