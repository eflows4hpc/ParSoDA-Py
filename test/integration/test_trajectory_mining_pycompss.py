
from parsoda.apps.trajectory_mining import build_trajectory_mining
from parsoda.function.crawling.distributed_file_crawler import DistributedFileCrawler
from parsoda.function.crawling.local_file_crawler import LocalFileCrawler
from parsoda.function.crawling.parsing.parsoda_parser import ParsodaParser
from parsoda.function.crawling.parsing.twitter_parser import TwitterParser
from parsoda.model.driver.parsoda_pycompss_driver import ParsodaPyCompssDriver

import unittest

class TestTrajectoryMiningPyCOMPSs(unittest.TestCase):
    
    def test_correctness(self):
        app = build_trajectory_mining(
            driver = ParsodaPyCompssDriver(),
            crawlers = [
                LocalFileCrawler('resources/input/test.json', ParsodaParser())
            ],
            rois_file="./resources/input/RomeRoIs.kml"
        )
        
        report = app.execute()
        
        self.assertGreaterEqual(report.get_reduce_result_length(), 10)
        
        
        
        