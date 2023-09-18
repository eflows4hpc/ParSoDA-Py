
from parsoda.apps.trajectory_mining import parsoda_trajectory_mining
from parsoda.function.crawling.distributed_file_crawler import DistributedFileCrawler
from parsoda.function.crawling.local_file_crawler import LocalFileCrawler
from parsoda.function.crawling.parsing.parsoda_parser import ParsodaParser
from parsoda.function.crawling.parsing.twitter_parser import TwitterParser
from parsoda.model.driver.parsoda_pycompss_driver import ParsodaPyCompssDriver

import unittest

class TestTrajectoryMiningPyCOMPSs(unittest.TestCase):
    
    def test_correctness(self):
        app = parsoda_trajectory_mining(
            driver = ParsodaPyCompssDriver(),
            crawlers = [
                LocalFileCrawler('resources/input/test.json', ParsodaParser())
            ],
            rois_file="./resources/input/RomeRoIs.kml",
            visualization_file="test_out/trajectory_mining.txt"
        )
        
        report = app.execute()
        
        self.assertEqual(report.get_reduce_result_length(), 1709)
        
        
        
        