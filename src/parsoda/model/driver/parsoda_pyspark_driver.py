from typing import Iterable, TypeVar, Optional
from pyspark import RDD, SparkContext, SparkConf
from parsoda.model.driver.parsoda_driver import ParsodaDriver
from parsoda.model.function.crawler import Crawler

class ParsodaPySparkDriver(ParsodaDriver):

    def __init__(self, spark_conf: SparkConf):
        self.num_partitions: Optional[int] = None
        self.rdd: Optional[RDD] = None
        self.spark_conf = spark_conf
        self.spark_context = SparkContext(conf=spark_conf)

    def init_environment(self):
        self.rdd = self.spark_context.emptyRDD()
        self.num_partitions = self.spark_context.defaultParallelism

    def set_num_partitions(self, num_partitions):
        self.num_partitions = num_partitions

    def crawl(self, crawlers: Iterable[Crawler]):
        for crawler in crawlers:
            partitions = crawler.get_partitions(self.num_partitions)
            if not crawler.supports_remote_partitioning():
                # master-located crawler
                crawler_rdd = self.spark_context.emptyRDD()
                for p in partitions:
                    p_rdd = self.spark_context.parallelize(p.retrieve_data(), numSlices=self.num_partitions)
                    crawler_rdd = crawler_rdd.union(p_rdd)
            else:
                # distributed crawler
                crawler_rdd = self.spark_context.parallelize(partitions, numSlices=len(partitions)) \
                    .flatMap(lambda p: p.retrieve_data())
            self.rdd = self.rdd.union(crawler_rdd)

    def filter(self, filter_func):
        self.rdd = self.rdd.filter(filter_func)

    def flatmap(self, mapper):
        self.rdd = self.rdd.flatMap(mapper)

    def sort_by_key(self) -> None:
        self.rdd = self.rdd.sortByKey(numPartitions=self.num_partitions)

    def group_by_key(self) -> None:
        self.rdd = self.rdd.groupByKey(numPartitions=self.num_partitions)
        pass

    def get_result(self):
        return self.rdd.collect()

    def dispose_environment(self):
        pass
