from __future__ import annotations

from abc import ABC
import math
from tracemalloc import start
from typing import IO, Any, Callable, List, Optional
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
        self.__text_lines: Optional[List[str]] = None
        self.__loaded = False

    def load_data(self) -> LocalFilePartition:
        if self.__loaded:
            return self
        data: List[str] = []
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
            text_line_len: int = len(text_line)
            read_bytes += text_line_len
            if text_line_len == 0:
                break
            text_line = text_line.strip()
            if text_line != '':
                data.append(text_line)
        self.__text_lines = data
        self.__loaded = True
        
        self.__file = None
        
        # clear the file handle, which is not useful anymore
        return self
    
    def parse_data(self) -> List[SocialDataItem]:
        if not self.__loaded:
            self.load_data()
        return [self.__parser(text_line) for text_line in self.__text_lines]
            

class LocalFileCrawler(Crawler, ABC):

    def __init__(self, file_path: str, parser: Parser):
        self.__file_path = file_path
        self.__file_len = os.path.getsize(self.__file_path)
        self.__parser = parser
        self.__file = open(file_path, "r", errors="ignore")

    def supports_remote_partitioning(self) -> bool:
        return False

    def get_partitions(self, num_of_partitions=0, partition_size=1024*1024*1024) -> List[CrawlerPartition]:
        print(f"[ParSoDA.LocalFileCrawler.get_partitions] file size={self.__file_len/(1024*1024):.2f} MB")
        print(f"[ParSoDA.LocalFileCrawler.get_partitions] "
              f"given number of partitions={num_of_partitions}; given partition size={partition_size/(1024*1024):.2f} MB")

        partitions: List[CrawlerPartition] = []

        if num_of_partitions is None or num_of_partitions <= 0:
            num_of_partitions = self.__file_len // partition_size
            chunk_sizes = [partition_size]*num_of_partitions
            reminder = self.__file_len % partition_size
            if reminder > 0:
                num_of_partitions += 1
                chunk_sizes.append(reminder)
        else:
            chunk_sizes = [self.__file_len // num_of_partitions]*num_of_partitions
            reminder = self.__file_len % num_of_partitions
            for i in range(reminder):
                chunk_sizes[i] += 1
            
        print(f"[ParSoDA.LocalFileCrawler.get_partitions] "
              f"computed number of partitions={num_of_partitions}; computed partition size={chunk_sizes[0]/(1024*1024):.2f} MB")
        print(f"[ParSoDA.LocalFileCrawler.get_partitions] "
              f"last partition size={chunk_sizes[-1]/(1024*1024):.2f} MB")

        start = 0
        for i in range(0, num_of_partitions):
            p = LocalFilePartition(self.__file, start, start+chunk_sizes[i], self.__parser)
            partitions.append(p)
            start += chunk_sizes[i]
        return partitions

    def close(self):
        if self.__file is not None:
            self.__file.close()
            self.__file = None

    def __del__(self):
        self.close()

