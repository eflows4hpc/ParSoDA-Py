from datetime import date
import sys
import argparse

from parsoda import SocialDataApp
from parsoda.function.analysis.gap_bide_analysis import GapBIDE
from parsoda.function.crawling.local_file_crawler import LocalFileCrawler
from parsoda.function.crawling.parsing.flickr_parser import FlickrParser
from parsoda.function.crawling.parsing.twitter_parser import TwitterParser
from parsoda.function.crawling.parsing.vinitaly2019_parser import Vinitaly2019Parser
from parsoda.function.filtering import IsInPlace, IsInRoI

from parsoda.function.mapping.find_poi import FindPoI
from parsoda.function.reduction.reduce_by_trajectories import ReduceByTrajectories
from parsoda.function.visualization.sort_gap_bide import SortGapBIDE
from parsoda.utils.roi import RoI

from parsoda.model.driver.parsoda_singlecore_driver import ParsodaSingleCoreDriver
from parsoda.model.driver.parsoda_multicore_driver import ParsodaMultiCoreDriver
from parsoda.model.driver.parsoda_pyspark_driver import ParsodaPySparkDriver

def parse_command_line():
    parser = argparse.ArgumentParser(description='Trajectory Mining application')
    parser.add_argument("--partitions", "-p",
                        type=int,
                        default=-1,
                        help="specifies the number of data partitions.")
    parser.add_argument("--chunk-size", "-c",
                        type=int,
                        default=128,
                        help="specifies the size of data partitions in megabytes.")
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_command_line()

    import pyspark
    driver = ParsodaPySparkDriver(pyspark.SparkConf())

    app = SocialDataApp("Trajectory Mining", driver, num_partitions=args.partitions, chunk_size=args.chunk_size)

    app.set_crawlers([
        #LocalFileCrawler('/root/tmpfs/TwitterRome2017.json', TwitterParser()) for i in range(3)
        LocalFileCrawler('/root/tmpfs/TwitterRome2017_6X.json', TwitterParser())
    ])
    app.set_filters([IsInRoI("./resources/input/RomeRoIs.kml")])
    app.set_mapper(FindPoI("./resources/input/RomeRoIs.kml"))
    app.set_secondary_sort_key(lambda x: x[0])
    app.set_reducer(ReduceByTrajectories(3))
    app.set_analyzer(GapBIDE(1, 0, 10))
    app.set_visualizer(
        SortGapBIDE(
            "./resources/output/trajectory_mining.txt", 
            'support', 
            mode='descending', 
            min_length=3
        )
    )

    app.execute()
