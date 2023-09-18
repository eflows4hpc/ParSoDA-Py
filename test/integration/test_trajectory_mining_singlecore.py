
from parsoda.apps.trajectory_mining import parsoda_trajectory_mining
from parsoda.function.crawling.distributed_file_crawler import DistributedFileCrawler
from parsoda.function.crawling.local_file_crawler import LocalFileCrawler
from parsoda.function.crawling.parsing.parsoda_parser import ParsodaParser
from parsoda.model.driver.parsoda_singlecore_driver import ParsodaSingleCoreDriver

import unittest

class TestTrajectoryMiningSingleCore(unittest.TestCase):
    
    def test_correctness(self):
        app = parsoda_trajectory_mining(
            driver = ParsodaSingleCoreDriver(),
            crawlers = [
                LocalFileCrawler('resources/input/test.json', ParsodaParser())
            ],
            rois_file="./resources/input/RomeRoIs.kml",
            visualization_file="test_out/trajectory_mining.txt"
        )
        report = app.execute()
        self.assertEqual(report.get_reduce_result_length(), 1709)
        
        
        
        