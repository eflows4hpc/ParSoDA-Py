
import unittest
import pyspark

from parsoda.apps.trajectory_mining import parsoda_trajectory_mining

from parsoda.function.crawling.local_file_crawler import LocalFileCrawler
from parsoda.function.crawling.parsing.parsoda_parser import ParsodaParser

from parsoda.model.driver.parsoda_pycompss_driver import ParsodaPyCompssDriver
from parsoda.model.driver.parsoda_pyspark_driver import ParsodaPySparkDriver
from parsoda.model.driver.parsoda_singlecore_driver import ParsodaSingleCoreDriver


class TestTrajectoryMining(unittest.TestCase):
    
    def trajectory_mining_testcase(self, driver):
        app = parsoda_trajectory_mining(
            driver = driver,
            crawlers = [
                LocalFileCrawler('resources/input/test.json', ParsodaParser())
            ],
            rois_file="./resources/input/RomeRoIs.kml",
            visualization_file="./resources/output/trajectory_mining.txt"
        )
        report = app.execute()
        self.assertEqual(report.get_reduce_result_length(), 1755)
    
    def test_singlecore(self):
        self.trajectory_mining_testcase(ParsodaSingleCoreDriver())
        
    def test_pyspark(self):
        ctx = pyspark.SparkContext(master="local[*]")
        self.trajectory_mining_testcase(ParsodaPySparkDriver(spark_context=ctx))
        ctx.stop()
        
    def test_pycompss(self):
        self.trajectory_mining_testcase(ParsodaPyCompssDriver())
        