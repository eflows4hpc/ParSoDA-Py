from __future__ import annotations
from abc import abstractmethod, ABC
from typing import Any, Callable, Iterable, List, Optional

from parsoda.model.social_data_item import SocialDataItem
    

class CrawlerPartition:
    """
    Defines an input data partition
    """
    
    @abstractmethod
    def load_data(self) -> CrawlerPartition:
        """
        Load all data of this partition
        """
        pass

    @abstractmethod
    def parse_data(self) -> List[SocialDataItem]:
        """
        Retrieves all social data items in this partition

        return: a list of social data items
        """
        pass


class Crawler(ABC):
    """
        Defines a crawler, i.e. a provider of SocialDataItem objects for a ParSoDA application.

        A crawler can be local or distributed. A local crawler is able to read data just on the master machine,
        where the ParSoDA application is started.
        A distributed crawler is able to read data from different remote partitions.

        Examples:
            A simple local crawler can read data from a local file in the master machine.
            A distributed crawler can load data from paged http requests to a web site that is accessible from
            each node of the cluster.
    """

    @abstractmethod
    def get_partitions(self, num_of_partitions=0, partition_size=1024*1024*1024) -> List[CrawlerPartition]:
        """
        IF the crawler does not support remote partitioning:
            It must return a list composed by one or more CrawlerPartition objects which allow to read all the data
            available to the crawler;

        ELSE if the crawler supports remote partitioning:
            Returns a list of CrawlerPartition objects that represents remotely readable partitions.
            Note that a remote partition must be readable regardless of which machine it is accessed from.

        REMOTE PARTITIONING:
            The crawler that supports remote partitioning is capable of splitting its data source
            in two or more partitions that can be read by any machine in a cluster.
            For example, remote partitioning can be used to implement crawlers that allow to retrieve
            data from one or more remote sites through http pagination,
            from HDFS (Hadoop Distributed FileSystem) partitions,
            or from any other distributed remote data source.
        """
        pass

    @abstractmethod
    def supports_remote_partitioning(self) -> bool:
        """Checks if the crawler supports remote partitioning, i.e. the ability to read data directly from the worker nodes

        Returns:
            bool: true if the crawler supports remote partitionig of data source.
        """
        pass


class MasterCrawler(Crawler):
    """
    Defines a crawler that loads SocialDataItem objects directly from the master node
    """

    def supports_remote_partitioning(self) -> bool:
        return False
    
class WorkerCrawler(Crawler):
    """
    Defines a crawler that loads SocialDataItem objects directly from the master node
    """

    def supports_remote_partitioning(self) -> bool:
        return True


class Parser(ABC):
    @abstractmethod
    def __call__(self, text_line: str) -> Optional[SocialDataItem]:
        pass
