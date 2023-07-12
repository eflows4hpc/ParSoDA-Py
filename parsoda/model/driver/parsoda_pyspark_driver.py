from typing import Iterable, List, Optional
from pyspark import RDD, SparkContext
from parsoda.model.driver.parsoda_driver import ParsodaDriver
from parsoda.model.function.crawler import Crawler, CrawlerPartition

class ParsodaPySparkDriver(ParsodaDriver):

    def __init__(self, spark_context: SparkContext):
        self.__chunk_size = None
        self.__num_partitions: Optional[int] = 64
        self.__rdd: Optional[RDD] = None
        self.__spark_context: SparkContext = spark_context

    def set_num_partitions(self, num_partitions):
        self.__num_partitions = num_partitions
        
    def set_chunk_size(self, chunk_size):
        self.__chunk_size = chunk_size

    def init_environment(self):
        self.__rdd = self.__spark_context.emptyRDD()

    def dispose_environment(self):
        self.__rdd = None

    def crawl(self, crawlers: Iterable[Crawler]):
        for crawler in crawlers:
            partitions: List[CrawlerPartition] = crawler.get_partitions(num_of_partitions=self.__num_partitions, partition_size=self.__chunk_size)
            if not crawler.supports_remote_partitioning():
                # master-located crawler
                print("[ParsodaPySparkDriver] reading from local crawler")
                for p in partitions:
                    p.load_data() # load on master, parse on worker
                    self.__rdd = self.__rdd.union(
                        self.__spark_context
                        .parallelize([p], numSlices=1)
                        .flatMap(lambda p: p.parse_data())
                    )
            else:
                # distributed crawler
                print("[ParsodaPySparkDriver] reading from distributed crawler")
                self.__rdd = self.__rdd.union(
                    self.__spark_context
                    .parallelize(partitions, numSlices=len(partitions))
                    .flatMap(lambda p: p.load_data().parse_data()) # load and parse on worker
                )
        
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
