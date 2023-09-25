
import unittest
import pyspark

from parsoda.apps.sentiment_analysis import parsoda_sentiment_analysis

from parsoda.function.crawling.local_file_crawler import LocalFileCrawler
from parsoda.function.crawling.parsing.parsoda_parser import ParsodaParser

from parsoda.model.driver.parsoda_pycompss_driver import ParsodaPyCompssDriver
from parsoda.model.driver.parsoda_pyspark_driver import ParsodaPySparkDriver
from parsoda.model.driver.parsoda_singlecore_driver import ParsodaSingleCoreDriver

    
def sentiment_analysis_testcase(driver):
    app = parsoda_sentiment_analysis(
        driver = driver,
        crawlers = [
            LocalFileCrawler('resources/input/test.json', ParsodaParser())
        ],
        emoji_file="./resources/input/emoji.json",
        visualization_file="./resources/output/sentiment_analysis.txt"
    )
    report = app.execute()
    return report.get_reduce_result_length()

class TestSentimentAnalysis(unittest.TestCase):
    expected_reduce_len: int = 0
    
    @classmethod
    def setUpClass(cls):
        cls.expected_reduce_len = sentiment_analysis_testcase(ParsodaSingleCoreDriver())
        
    def test_pyspark(self):
        ctx = pyspark.SparkContext(master="local[*]")
        computed_reduce_len = sentiment_analysis_testcase(ParsodaPySparkDriver(spark_context=ctx))
        ctx.stop()
        self.assertEqual(computed_reduce_len, TestSentimentAnalysis.expected_reduce_len)
        
    def test_pycompss(self):
        computed_reduce_len = sentiment_analysis_testcase(ParsodaPyCompssDriver())
        self.assertEqual(computed_reduce_len, TestSentimentAnalysis.expected_reduce_len)
        