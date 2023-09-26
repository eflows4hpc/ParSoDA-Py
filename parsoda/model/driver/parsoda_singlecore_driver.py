import os
from typing import Any, Callable, Dict, List, TypeVar

from parsoda import SocialDataItem
from parsoda.model import ParsodaDriver, Crawler, Filter, Mapper, Reducer

path_service_file = "./.parsoda_pycompss_serviceFile.json"


class ParsodaSingleCoreDriver(ParsodaDriver):

    def __init__(self):
        self.dataset = None
        self.num_partitions = 0
        self.chunk_size = 64*1024*1024

    def init_environment(self):
        self.dataset = list()

    def set_num_partitions(self, num_partitions):
        self.num_partitions = num_partitions
        
    def set_chunk_size(self, chunk_size):
        self.chunk_size = chunk_size

    def crawl(self, crawlers: List[Crawler]):
        for crawler in crawlers:
            partitions = crawler.get_partitions(num_of_partitions=self.num_partitions, partition_size=self.chunk_size)
            for p in partitions:
                for item in p.load_data().parse_data():
                    self.dataset.append(item)

    def filter(self, filter_func):
        filtered = list()
        for item in self.dataset:
            if filter_func(item):
                filtered.append(item)
        self.dataset = filtered

    def flatmap(self, mapper):
        mapped = list()
        for item in self.dataset:
            mapped.extend(mapper(item))
        self.dataset = mapped

    def sort_by_key(self) -> None:
        self.dataset.sort(key=lambda x: x[0])

    def group_by_key(self):
        result: Dict[Any, List] = {}
        for kv_pair in self.dataset:
            k = kv_pair[0]
            v = kv_pair[1]
            if k in result:
                result[k].append(v)
            else:
                result[k] = [v]
        self.dataset = result.items()

    def get_result(self):
        return self.dataset

    def dispose_environment(self):
        self.dataset = None
