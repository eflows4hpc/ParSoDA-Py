import os
from collections import Callable
from typing import List, TypeVar, Optional
from parsoda.model.function.crawler import CrawlerPartition

from pycompss.dds import DDS

from parsoda import SocialDataItem
from parsoda.model import ParsodaDriver, Crawler, Filter, Mapper, Reducer


class ParsodaPyCompssDriver(ParsodaDriver):

    def __init__(self):
        self.num_partitions: Optional[int] = None
        self.dds: Optional[DDS] = None

    def init_environment(self):
        self.dds = DDS()
        self.num_partitions = 8

    def set_num_partitions(self, num_partitions):
        self.num_partitions = num_partitions

    def crawl(self, crawlers: List[Crawler]):
        for crawler in crawlers:
            partitions = crawler.get_partitions(self.num_partitions)
            if not crawler.supports_remote_partitioning():
                # master-located crawler
                for p in partitions:
                    crawler_dds = DDS().load(p.retrieve_data(), num_of_parts=self.num_partitions)
                    self.dds = self.dds.union(crawler_dds)
            else:
                # distributed crawler
                crawler_dds = DDS() \
                    .load(partitions, num_of_parts=len(partitions)) \
                    .flat_map(lambda p: p.retrieve_data())  # flat-maps a partition to its data
                self.dds = self.dds.union(crawler_dds)

    def filter(self, filter_func):
        self.dds = self.dds.filter(filter_func)

    def flatmap(self, mapper):
        self.dds = self.dds.flat_map(mapper)

    def map(self, mapper):
        self.dds = self.dds.map(mapper)

    def sort_by_key(self) -> None:
        self.dds = self.dds.sort_by_key()
        pass

    def group_by_key(self) -> None:
        self.dds = self.dds.group_by_key(num_of_parts=self.num_partitions)

    def get_result(self):
        return self.dds.collect(keep_partitions=False, future_objects=False)

    def dispose_environment(self):
        pass
