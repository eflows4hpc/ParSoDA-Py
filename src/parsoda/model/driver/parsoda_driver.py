from abc import abstractmethod, ABC
from typing import Callable, Iterable, Any, List

from parsoda.model.function.crawler import Crawler


class ParsodaDriver(ABC):
    """
    Defines a driver interface that is an implementor of the SocialDataApp abstraction of ParSoDA (Bridge pattern).
    A ParSoDA driver implements the first five steps of ParSoDA
    on a given system (e.g., Spark, PyCompss, Hadoop, Posix threads or GPUs)

    Each operation is inteded to produce a new dataset and replace the previous one.
    """

    @abstractmethod
    def init_environment(self) -> None:
        """
        Initializes the execution environment (e.g., creates a new RDD on Spark)
        """
        pass

    @abstractmethod
    def set_num_partitions(self, num_partitions) -> None:
        """
        Sets the number of data partitions
        :return: None
        """
        pass

    @abstractmethod
    def crawl(self, crawler: List[Crawler]) -> None:
        """
        Collects the data from crawlers.
        For each crawler that supports remote partitioning:
            if the underlying environment is distributed, this method might implement data reading from
            each partiton directly on the nodes of a cluster.
        For each crawler that does not support remote partitioning:
            the underlying system retrieves data directly from it.
        Anyway, partitioning might be executed just after loading data from all crawlers.

        After invoking this function the implementor should hold a representation of an initial dataset
        (e.g., on Spark a new RDD is populated with the SocialDataItem objects provided by crawlers)
        :return: None
        """
        pass

    @abstractmethod
    def filter(self, filter_func: Callable[[Any], bool]) -> None:
        """
        Applies the given filter to the current dataset, dropping all items that does not satisfy the filter
        :param filter_func: the filter to apply
        :return: None
        """
        pass

    @abstractmethod
    def flatmap(self, mapper: Callable[[Any], Iterable[Any]]) -> None:
        """
        Executes a mapping of each item to a list of custom key-value pairs, represented as tuples of two elements each
        :param mapper: the (object -> list[(K,V)]) mapping function to apply
        :return: None
        """
        pass

    def map(self, mapper: Callable[[Any], Any]) -> None:
        """
        Executes a mapping of each item in the current dataset to a new object
        :param mapper: the (object -> list[(K,V)]) mapping function to apply
        :return: None
        """
        self.flatmap(lambda item: [mapper(item)])

    @abstractmethod
    def sort_by_key(self) -> None:
        """
        Sorts by key all the items of the current dataset as key-value pairs, represented as tuples of two elements each.
        :return: None
        """
        pass

    #TODO: documentation
    def group_by_key(self) -> None:
        pass

    # def combine_by_key(self, mapper: Callable[[Any], Iterable[Any]], combiner: reducer: Callable[[Any, Any], Any]):
    #   pass

    def get_result(self) -> Any:
        """
        Gets the current dataset
        :return: the current dataset
        """
        pass

    @abstractmethod
    def dispose_environment(self) -> None:
        """
        Disposes instantiated resources of the underlying environment, after executing the ParSoDA application
        :return: None
        """
        pass
