from datetime import date
import os
import sys
import argparse
from typing import List, Tuple

import pyspark

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
from parsoda.model.driver.parsoda_driver import ParsodaDriver
from parsoda.model.driver.parsoda_multicore_driver import ParsodaMultiCoreDriver
from parsoda.model.driver.parsoda_pyspark_driver import ParsodaPySparkDriver
from parsoda.utils.roi import RoI

from parsoda.model.driver.parsoda_singlecore_driver import ParsodaSingleCoreDriver
from parsoda.model.driver.parsoda_pycompss_driver import ParsodaPyCompssDriver

supported_formats = {
    "twitter": TwitterParser(),
    "flickr": FlickrParser(),
    "vinitaly2019": Vinitaly2019Parser(),
}

def mine_trajectories(
    input_files: List[Tuple[str, str]], 
    rois_file: str,
    driver: ParsodaDriver,
    *, 
    num_partitions=-1, 
    chunk_size=128, 
    min_trajectory_length=3,  
    min_support=1, 
    min_gap=0, 
    max_gap=10, 
    visualization_file="trajectory_mining.txt",
    visualization_min_length=3
):
    driver = ParsodaPyCompssDriver()
    
    app = SocialDataApp("Trajectory Mining", driver, num_partitions=num_partitions, chunk_size=chunk_size)
    
    app.set_crawlers(
        [LocalFileCrawler(file_path, supported_formats[file_format]) for file_format, file_path in input_files]
    )
    app.set_filters([
        IsInRoI(rois_file)
    ])
    app.set_mapper(FindPoI(rois_file))
    app.set_secondary_sort_key(lambda x: x[0])
    app.set_reducer(ReduceByTrajectories(min_trajectory_length))
    app.set_analyzer(GapBIDE(min_support, min_gap, max_gap))
    app.set_visualizer(
        SortGapBIDE(
            visualization_file, 
            'support', 
            mode='descending', 
            min_length=visualization_min_length
        )
    )

    app.execute()


def parse_command_line():
    def type_parsoda_driver(arg: str) -> ParsodaDriver:
        if arg == "pyspark":
            return ParsodaPySparkDriver(pyspark.SparkConf())
        elif arg == "pycompss":
            return ParsodaPyCompssDriver()
        elif arg == "singlecore":
            return ParsodaSingleCoreDriver()
        elif arg.startswith("multicore"):
            arg = arg.split(":", maxsplit=1)
            if len(arg)==2:
                num_cores = int(arg[1])
            else:
                num_cores = -1
            return ParsodaMultiCoreDriver(num_cores)
        
        raise argparse.ArgumentTypeError(f"ParsodaDriver \"{arg}\" unrecognized.")
            
    def type_input_file(arg: str) -> Tuple[str, str]:
        try:
            file_format, file_path = map(int, arg.split(':', maxsplit=1))
            return file_format, file_path
        except:
            raise argparse.ArgumentTypeError(f"input file must be in the form <format-tag>:<file-path>, but the following was found: {arg}")
    
    parser = argparse.ArgumentParser(description='Trajectory Mining application')
    parser.add_argument(
        "input_files",
        nargs="+",
        type=type_input_file,
        help="specifies a list of input json files. "
            "Each item of the list is a string composed by a format tag and a file path: <format-tag>:<file-path>.\n"
            f"supported formats are: {supported_formats.keys()}"
    )
    parser.add_argument(
        "rois_file",
        type=str,
        help="specifies a file containing Regions of Interest (RoI)."
    )
    parser.add_argument(
        "parsoda_driver",
        type=type_parsoda_driver,
        help="specifies the ParSoDA driver for the underlying execution environment.\n"
            "Possible choices are: 'pycompss', 'pyspark', 'singlecore', 'multicore:<number-of-workers>'\n"
            "<number-of-workers> can be any number. 0 and all negative numbers set the numer of workers to the same value of the number of cores in the local system. (Examples: multicore:8, multicore:1, multicore:0)"
    )
    parser.add_argument(
        "--partitions", "-p",
        type=int,
        default=-1,
        help="specifies the number of data partitions."
    )
    parser.add_argument(
        "--chunk-size", "-c",
        type=int,
        default=128,
        help="specifies the size of data partitions in megabytes."
    )
    # TODO: add other algorithm parameters (min_trajectory_length, min_support, etc.)
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_command_line()
    mine_trajectories(
        args.input_files, 
        args.rois_file, 
        args.parsoda_driver, 
        num_partitions=args.partitions, 
        chunk_size=args.chunk_size
    )

    
