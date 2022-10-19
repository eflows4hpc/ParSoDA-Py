import math
import os
from collections import Callable
from typing import List, TypeVar, Optional
from parsoda.model.function.crawler import CrawlerPartition

from pycompss.dds import DDS

from parsoda import SocialDataItem
from parsoda.model import ParsodaDriver, Crawler, Filter, Mapper, Reducer


class ParsodaPyCompssDriver(ParsodaDriver):

    def __init__(self):
        self.__chunk_size = None
        self.__num_partitions: Optional[int] = None
        self.__dds: Optional[DDS] = None

    def init_environment(self):
        self.__dds = DDS()
        self.__num_partitions = 0
        self.__chunk_size = 128*1024*1024
        
    def set_chunk_size(self, chunk_size: int):
        self.__chunk_size = chunk_size

    def set_num_partitions(self, num_partitions):
        self.__num_partitions = num_partitions

    def crawl(self, crawlers: List[Crawler]):
        num_partitions_per_crawler = math.ceil(self.__num_partitions/len(crawlers))
        for crawler in crawlers:
            partitions: List[CrawlerPartition] = crawler.get_partitions(num_partitions_per_crawler, self.__chunk_size)
            if not crawler.supports_remote_partitioning():
                # master-located crawler, we must load partitions locally
                for p in partitions:
                    p.load_data()
                    crawler_dds = (
                        DDS()
                        .load([p], num_of_parts=1)
                        .flat_map(lambda partition: partition.parse_data())
                    )
                    self.__dds = self.__dds.union(crawler_dds)
            else:
                # distributed crawler, we can load a data partition on a remote worker, in order to balance the reading load
                crawler_dds = (
                    DDS()
                    .load(partitions, num_of_parts=len(partitions))
                    .flat_map(lambda p: p.load_data().parse_data())  # flat-maps a partition to its data
                )
                self.__dds = self.__dds.union(crawler_dds)

    def filter(self, filter_func):
        self.__dds = self.__dds.filter(filter_func)

    def flatmap(self, mapper):
        self.__dds = self.__dds.flat_map(mapper)

    def map(self, mapper):
        self.__dds = self.__dds.map(mapper)

    def sort_by_key(self) -> None:
        self.__dds = self.__dds.sort_by_key()
        pass

    def group_by_key(self) -> None:
        self.__dds = self.__dds.group_by_key()

    def get_result(self):
        return self.__dds.collect(keep_partitions=False, future_objects=False)

    def dispose_environment(self):
        pass
