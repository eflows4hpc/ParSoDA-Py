import math
from typing import Iterable, TypeVar, Optional
from pyspark import RDD, SparkContext, SparkConf
from parsoda.model.driver.parsoda_driver import ParsodaDriver
from parsoda.model.function.crawler import Crawler

class ParsodaPySparkDriver(ParsodaDriver):

    def __init__(self, spark_conf: SparkConf):
        self.__chunk_size = 64*1024*1024
        self.__num_partitions: Optional[int] = None
        self.__rdd: Optional[RDD] = None
        self.__spark_conf = spark_conf
        self.__spark_context = SparkContext(conf=spark_conf)

    def init_environment(self):
        self.__rdd = self.__spark_context.emptyRDD()
        self.__num_partitions = self.__spark_context.defaultParallelism

    def set_num_partitions(self, num_partitions):
        self.__num_partitions = num_partitions
        
    def set_chunk_size(self, chunk_size):
        self.__chunk_size = chunk_size

    def crawl(self, crawlers: Iterable[Crawler]):
        num_partitions_per_crawler = math.ceil(self.__num_partitions/len(crawlers))
        for crawler in crawlers:
            partitions = crawler.get_partitions(num_partitions_per_crawler, self.__chunk_size)
            if not crawler.supports_remote_partitioning():
                # master-located crawler
                crawler_rdd = self.__spark_context.emptyRDD()
                for p in partitions:
                    p.load_data()
                    crawler_rdd = (
                        self.__spark_context
                        .parallelize([p], numSlices=self.__num_partitions)
                        .flatMap(lambda p: p.parse_data())
                    )
                    self.__rdd = self.__rdd.union(crawler_rdd)
            else:
                # distributed crawler
                self.__rdd = self.__rdd.union(
                    self.__spark_context
                    .parallelize(partitions, numSlices=len(partitions))
                    .flatMap(lambda p: p.load_data().parse_data())
                )
                self.__rdd = self.__rdd.union(crawler_rdd)
        
    def filter(self, filter_func):
        self.__rdd = self.__rdd.filter(filter_func)

    def flatmap(self, mapper):
        self.__rdd = self.__rdd.flatMap(mapper)

    def sort_by_key(self) -> None:
        self.__rdd = self.__rdd.sortByKey() #can specify the number of partition

    def group_by_key(self) -> None:
        self.__rdd = self.__rdd.groupByKey() #can specify the number of partition
        pass

    def get_result(self):
        return self.__rdd.collect()

    def dispose_environment(self):
        pass
