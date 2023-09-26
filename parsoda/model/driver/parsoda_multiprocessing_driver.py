import multiprocessing
from multiprocessing.pool import AsyncResult
import os
import queue
from typing import Optional, List, Tuple, Dict

from parsoda.model import ParsodaDriver, Crawler, Filter, Mapper, Reducer
from multiprocessing import Pool

from parsoda.model.function.crawler import CrawlerPartition

def _task_load(p: CrawlerPartition):
    return p.load_data().parse_data()

def _task_filter(filter_func, partition: List):
    #print(f"_task_filter: partition={partition}")
    filtered_partition = []
    for item in partition:
        if filter_func(item):
            filtered_partition.append(item)
    return filtered_partition

def _task_map(mapper, partition: List):
    mapped_partition = []
    for item in partition:
        mapped_partition.extend(mapper(item))
    return mapped_partition

def _task_sort(partition: List, key=lambda kv: kv[0]):
    partition.sort()
    return partition

def _task_reduce(reducer, partition: List[Tuple]):
    reduce_result = Dict()
    for kv in partition:
        k, v = kv[0], kv[1]
        if k in reduce_result:
            reduce_result[k] = reducer(reduce_result[k], v)
        else:
            reduce_result[k] = v
    return reduce_result

def _task_group(partition: List[Tuple])->Dict:
    result = {}
    for k, v in partition:
        if k in result:
            result[k].append(v)
        else:
            result[k] = [v]
    return result

class ParsodaMultiprocessingDriver(ParsodaDriver):

    def __init__(self, parallelism: int = -1):
        self.__parallelism = parallelism if parallelism>0 else multiprocessing.cpu_count()
        self.__dataset: Optional[list] = None
        self.__num_partitions = parallelism if parallelism>0 else multiprocessing.cpu_count()
        self.__chunk_size = 0
        self.__pool: Pool = None

    def init_environment(self):
        self.__dataset = []
        self.__pool = multiprocessing.Pool(self.__parallelism)

    def set_num_partitions(self, num_partitions):
        self.__num_partitions = num_partitions
        
    def set_chunk_size(self, chunk_size):
        self.__chunk_size = chunk_size
    
    def __partitioning(self, merged):
        if self.__num_partitions is None or self.__num_partitions <= 0:
            chunk_size = self.__chunk_size if self.__chunk_size>0 else 64
            num_of_partitions = len(merged) // chunk_size
            chunk_sizes = [chunk_size]*num_of_partitions
            reminder = len(merged) % chunk_size
            if reminder > 0:
                num_of_partitions += 1
                chunk_sizes.append(reminder)
        else:
            num_of_partitions = self.__num_partitions
            chunk_sizes = [len(merged) // num_of_partitions]*num_of_partitions
            reminder = len(merged) % num_of_partitions
            for i in range(reminder):
                chunk_sizes[i] += 1
        
        partitions = []
        start = 0
        for i in range(0, num_of_partitions):
            p = merged[start : start+chunk_sizes[i]]
            partitions.append(p)
            start += chunk_sizes[i]
        self.__dataset = partitions

    def crawl(self, crawlers: List[Crawler]):
        self.__pool: multiprocessing.Pool
        futures = []
        for crawler in crawlers:
            crawler_partitions = crawler.get_partitions(self.__num_partitions, self.__chunk_size)
            for p in crawler_partitions:
                future: AsyncResult = self.__pool.apply_async(func=_task_load, args=(p,))
                futures.append(future)

        for future in futures:
            self.__dataset.append(future.get())

    def filter(self, filter_func):
        filtered_partitions = []
        futures = []

        for p in self.__dataset:
            future = self.__pool.apply_async(_task_filter, (filter_func, p))
            futures.append(future)

        for future in futures:
            filtered_partitions.append(future.get())
        self.__dataset = filtered_partitions

    def flatmap(self, mapper):
        mapped_partitions = []
        futures = []
        
        #self.__dataset = self.__pool.map(_task_map, self.__dataset, 1)

        for p in self.__dataset:
            future = self.__pool.apply_async(_task_map, (mapper, p))
            futures.append(future)

        for future in futures:
            mapped_partitions.append(future.get())
        self.__dataset = mapped_partitions
        
    def group_by_key(self):
        futures = []

        def combine(accumulator: dict, partition: dict):
            for k, vs in partition.items():
                if k in accumulator:
                    accumulator[k].extend(vs)
                else:
                    accumulator[k] = vs
                    
        grouped_partitions = self.__pool.map(_task_group, self.__dataset, 1)
        
        accumulator = {}
        for p in grouped_partitions:
            combine(accumulator, p)
            

        # for p in self.__dataset:
        #     future = self.__pool.apply_async(_task_group, (p,))
        #     futures.append(future)

        # accumulator = {}
        # for future in futures:
        #     grouped_partition: dict = future.get()
        #     combine(accumulator, grouped_partition)
        result = [(k,v) for k, v in accumulator.items()]
        print(f"grouped={result}")
        self.__partitioning(result)

    def get_result(self):
        result = []
        for p in self.__dataset:
            result.extend(p)
        return result

    def dispose_environment(self):
        self.__dataset = None
        self.__pool.close()
        self.__pool = None
