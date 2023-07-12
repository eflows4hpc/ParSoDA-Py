import math
import os
from collections import Callable
from typing import List, TypeVar, Optional
from parsoda.model.function.crawler import CrawlerPartition

from pycompss.api.task import task
from pycompss.dds import DDS
from pycompss.api.api import compss_barrier

from parsoda import SocialDataItem
from parsoda.model import ParsodaDriver, Crawler, Filter, Mapper, Reducer


class ParsodaPyCompssTaskDriver(ParsodaDriver):

    def __init__(self):
        self.__chunk_size = None
        self.__num_partitions: Optional[int] = 8
        self.__partitions: Optional[List] = None
        
    def set_chunk_size(self, chunk_size: int):
        self.__chunk_size = chunk_size

    def set_num_partitions(self, num_partitions):
        self.__num_partitions = num_partitions

    def init_environment(self):
        self.__partitions = []*self.__num_partitions

    def dispose_environment(self):
        self.__partitions = None

    def crawl(self, crawlers: List[Crawler]):
        
        @task(returns=list)
        def _task_load_and_parse(partition: CrawlerPartition)->list:
            return partition.load_data().parse_data()
        
        @task(returns=list)
        def _task_parse(partition: CrawlerPartition)->list:
            return partition.parse_data()
        
        for crawler in crawlers:
            partitions: List[CrawlerPartition] = crawler.get_partitions(num_of_partitions=self.__num_partitions, partition_size=self.__chunk_size)
            if not crawler.supports_remote_partitioning():
                # master-located crawler, we must load partitions locally
                for p in partitions:
                    p.load_data()
                    p_data = _task_parse(p)
                    self.__partitions.append(p_data)
            else:
                # distributed crawler, we can load each data partition on a remote worker, in order to balance the reading workload
                for p in partitions:
                    p_data = _task_load_and_parse(p)
                    self.__partitions.append(p_data)
        #compss_barrier()
        
    def __map_partitions(self, partition_mapper, partitions):
        @task(returns=list)
        def _task_map(partition: list)->list:
            result = partition_mapper(partition)
        for i in range(len(self.__partitions)):
            partitions[i] = _task_map(partitions[i])

    def filter(self, filter_func):
        def mapper_filter(partition: list)->list:
            result = []
            for item in partition:
                if filter_func(item):
                    result.append(item)
            return result
        self.__map_partitions(mapper_filter)
        

    def flatmap(self, mapper):
        def mapper_flatmap(p):
            result = []
            for item in p:
                result.extend(mapper(item))
            return result
        self.__map_partitions(mapper_flatmap)

    #TODO

    # def sort_by_key(self) -> None:
    #     pass

    def group_by_key(self) -> None:
        self.__dds = self.__dds.group_by_key()

    def get_result(self):
        return self.__dds.collect(keep_partitions=False, future_objects=False)
