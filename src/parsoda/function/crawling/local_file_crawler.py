from abc import ABC
import math
from tracemalloc import start
from typing import IO, List
import os

from parsoda.model.function.crawler import Crawler, CrawlerPartition, MasterCrawler
from parsoda.model import Parser
from parsoda.model.social_data_item import SocialDataItem


class LocalFilePartition(CrawlerPartition, ABC):

    def __init__(self, file: IO, start: int, end: int, parser: Parser) -> None:
        self.__file = file
        self.__start = start
        self.__end = end
        self.__parser = parser

    def retrieve_data(self) -> List[SocialDataItem]:
        data: List[SocialDataItem] = []
        read_bytes = 0

        # if we are in the middle of a text line, we skip it
        if self.__start != 0:
            self.__file.seek(self.__start-1)
            start_char = self.__file.read(1)
            if start_char != '\n':
                half_line = self.__file.readline() # skip the half line
                read_bytes+=len(half_line)

        # loop over the interesting file portion
        while self.__start+read_bytes < self.__end:
            text_line: str = self.__file.readline()
            read_bytes += len(text_line)
            if text_line == '':
                break
            text_line = text_line.strip()
            if text_line != '':
                item = self.__parser(text_line)
                data.append(item)
        return data


class LocalFileCrawler(Crawler, ABC):

    def __init__(self, file_path: str, parser: Parser):
        self.__file_path = file_path
        self.__file_len = os.path.getsize(self.__file_path)
        self.__parser = parser
        self.__file = open(file_path, "r")

    def supports_remote_partitioning(self) -> bool:
        return False

    def get_partitions(self, num_of_partitions) -> List[CrawlerPartition]:
        print(f"[ParSoDA.LocalFileCrawler] get_partitions({num_of_partitions})")
        partitions: List[CrawlerPartition] = []
        partition_size = 4*1024*1024*1024 # 4 gigabytes chunk
        num_partitions = math.ceil(1.0 * self.__file_len / partition_size)
        #print(f"[LocalFileCrawler:{self.__file_path}] num_partitions={num_partitions}")
        for i in range(0, num_partitions):
            #print(f"[LocalFileCrawler:{self.__file_path}] creating partition {i}: {partition_size*i}-{partition_size*(i+1)}")
            p = LocalFilePartition(self.__file, partition_size*i, partition_size*(i+1), self.__parser)
            partitions.append(p)
        return partitions

    def close(self):
        if self.__file is not None:
            self.__file.close()
            self.__file = None

    def __del__(self):
        self.close()

