from datetime import date
import sys

from parsoda.apps.trajectory_mining import parsoda_trajectory_mining
from parsoda.function.crawling.distributed_file_crawler import DistributedFileCrawler
from parsoda.function.crawling.local_file_crawler import LocalFileCrawler
from parsoda.function.crawling.parsing.flickr_parser import FlickrParser
from parsoda.function.crawling.parsing.parsoda_parser import ParsodaParser
from parsoda.function.crawling.parsing.twitter_parser import TwitterParser
from parsoda.function.crawling.parsing.vinitaly2019_parser import Vinitaly2019Parser

from test.usecase.parsoda_usecase_parameters import ParsodaUseCaseParameters


if __name__ == '__main__':
    test = ParsodaUseCaseParameters()
    app = parsoda_trajectory_mining(
        driver = test.driver,
        crawlers = [
            DistributedFileCrawler('/storage/dataset/TwitterRome2017_6X.json', TwitterParser())
        ],
        rois_file="./resources/input/RomeRoIs.kml",
        num_partitions=test.partitions, 
        chunk_size=test.chunk_size
    )
    app.execute()
    
