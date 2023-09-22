
import unittest
import pyspark

from parsoda.apps.sentiment_analysis import parsoda_sentiment_analysis

from parsoda.function.crawling.local_file_crawler import LocalFileCrawler
from parsoda.function.crawling.parsing.parsoda_parser import ParsodaParser

from parsoda.model.driver.parsoda_pycompss_driver import ParsodaPyCompssDriver
from parsoda.model.driver.parsoda_pyspark_driver import ParsodaPySparkDriver
from parsoda.model.driver.parsoda_singlecore_driver import ParsodaSingleCoreDriver


class TestSentimentAnalysis(unittest.TestCase):
    
    def sentiment_analysis_testcase(self, driver):
        app = parsoda_sentiment_analysis(
            driver = driver,
            crawlers = [
                LocalFileCrawler('resources/input/test.json', ParsodaParser())
            ],
            emoji_file="./resources/input/emoji.json",
            visualization_file="./resources/output/trajectory_mining.txt"
        )
        report = app.execute()
        self.assertEqual(report.get_reduce_result_length(), 578)
    
    def test_singlecore(self):
        self.sentiment_analysis_testcase(ParsodaSingleCoreDriver())
        
    def test_pyspark(self):
        ctx = pyspark.SparkContext(master="local[*]")
        self.sentiment_analysis_testcase(ParsodaPySparkDriver(spark_context=ctx))
        ctx.stop()
        
    def test_pycompss(self):
        self.sentiment_analysis_testcase(ParsodaPyCompssDriver())
        