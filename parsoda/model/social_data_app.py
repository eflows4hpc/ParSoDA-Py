import locale
from abc import abstractmethod
from optparse import Values
from typing import Iterable, TypeVar, Generic, Any, Callable, Protocol, Optional, List, Dict

from parsoda.model.driver.parsoda_driver import ParsodaDriver
from parsoda.model.function.crawler import Crawler
from parsoda.model.function.visualizer import Visualizer
from parsoda.model import Filter, Mapper, Reducer, Analyzer
from parsoda.utils.stopwatch import StopWatch

class ParsodaReport:

    def __init__(
        self, 
        app_name, 
        driver, 
        partitions, 
        chunk_size, 
        crawling_time, 
        filter_time, 
        map_time, 
        split_time, 
        reduce_time, 
        analysis_time, 
        visualization_time,
        reduce_result_length
    ):
        self.__app_name = app_name
        self.__driver = driver
        self.__partitions = int(partitions)
        self.__chunk_size = int(chunk_size)
        self.__crawling_time = crawling_time
        self.__filter_time = filter_time
        self.__map_time = map_time
        self.__split_time = split_time
        self.__reduce_time = reduce_time
        self.__analysis_time = analysis_time
        self.__visualization_time = visualization_time

        self.__filter_to_reduce_time = filter_time + map_time + split_time + reduce_time
        self.__total_execution_time = self.__filter_to_reduce_time + analysis_time + visualization_time
        self.__total_time = crawling_time + self.__total_execution_time
        
        self.__reduce_result_length = reduce_result_length
                     
    def get_app_name(self):
        return self.__app_name
        
    def get_driver(self):
        return self.__driver
        
    def get_partitions(self):
        return self.__partitions
    
    def get_chunk_size(self):
        return self.__chunk_size
        
    def get_crawling_time(self):
        return self.__crawling_time
        
    def get_filter_time(self):
        return self.__filter_time
        
    def get_map_time(self):
        return self.__map_time
        
    def get_split_time(self):
        return self.__split_time
        
    def get_reduce_time(self):
        return self.__reduce_time
        
    def get_analysis_time(self):
        return self.__analysis_time
        
    def get_visualization_time(self):
        return self.__visualization_time

    def get_total_execution_time(self):
        return self.__filter_to_reduce_time

    def get_total_execution_time(self):
        return self.__total_execution_time
        
    def get_total_time(self):
        return self.__total_time
        
    def get_reduce_result_length(self):
        return self.__reduce_result_length

    def __repr__(self):
        return str(self)
        
    def __str__(self):
        return "\n" + \
        "\n" + \
        "| [ParSoDA Application Report]\n" + \
        "|" + "\n" + \
        "| App name: " + self.__app_name + "\n" + \
        "| ParSoDA Driver: " + type(self.__driver).__name__ + "\n" + \
        "| Data partitions: " + str(self.__partitions) + "\n" + \
        "| Chunk size: " + str(self.__chunk_size) + "\n" + \
        "|" + "\n" + \
        "| Crawling execution time: " + str(self.__crawling_time) + "\n" + \
        "| Filtering execution time: " + str(self.__filter_time) + "\n" + \
        "| Mapping execution time: " + str(self.__map_time) + "\n" + \
        "| Splitting execution time: " + str(self.__split_time) + "\n" + \
        "| Reduction execution time: " + str(self.__reduce_time) + "\n" + \
        "| Analysis execution time: " + str(self.__analysis_time) + "\n" + \
        "| Visualization execution time: " + str(self.__visualization_time) + "\n" + \
        "|" + "\n" + \
        "| Total Filter-To-Reduce time: " + str(self.__filter_to_reduce_time) + "\n" + \
        "| Total execution time: " + str(self.__total_execution_time) + "\n" + \
        "| Total time: " + str(self.__total_time) + "\n" \
        "|" + "\n" + \
        "| Reduce result length: " + str(self.__reduce_result_length) + "\n"
    
    def to_csv_line(self, separator: str = ";") -> str:
        return \
            str(self.__app_name)+separator+\
            str(self.__partitions)+separator+\
            str(self.__chunk_size)+separator+\
            str(self.__crawling_time)+separator+\
            str(self.__filter_time)+separator+\
            str(self.__map_time)+separator+\
            str(self.__split_time)+separator+\
            str(self.__reduce_time)+separator+\
            str(self.__analysis_time)+separator+\
            str(self.__visualization_time)+separator+\
            str(self.__filter_to_reduce_time)+separator+\
            str(self.__total_execution_time)+separator+\
            str(self.__total_time)+separator+\
            str(self.__reduce_result_length)
    
    def to_csv_titles(self, separator: str = ";") -> str:
        return \
            "App Name"+separator+\
            "Partitions"+separator+\
            "Chunk Size"+separator+\
            "Crawling Time"+separator+\
            "Filter Time"+separator+\
            "Map Time"+separator+\
            "Split Time"+separator+\
            "Reduce Time"+separator+\
            "analysis Time"+separator+\
            "Visualization Time"+separator+\
            "Filter to Reduce Time"+separator+\
            "Execution Time"+separator+\
            "Total Time"+separator+\
            "Reduce Result Length"
        

class SupportsLessThan(Protocol):
    @abstractmethod
    def __lt__(self, other):
        pass


K = TypeVar("K")  # key type resulting from mapping
V = TypeVar("V")  # value type resulting from mapping
R = TypeVar("R")  # reduction output type (might be equal to V)
A = TypeVar("A")  # analysis output type
SORTABLE_KEY = TypeVar("SORTABLE_KEY", bound=SupportsLessThan)  # generic types that supports the "less than" operator

def _filter_none(item):
    return item is not None

class _sort_kvs():
    def __init__(self, secondary_key):
        self.__secondary_key = secondary_key
    def __call__(self, kvs):
        return (kvs[0], sorted(kvs[1], key=self.__secondary_key))

class _reduce():
    def __init__(self, reducer):
        self.__reducer = reducer
    def __call__(self, kv):
        return (kv[0], self.__reducer.reduce(kv[0], kv[1]))

def _filter_kv_none(kv):
    return kv[1] is not None

class SocialDataApp(Generic[K, V, R, A]):

    def __init__(self, app_name: str, driver: ParsodaDriver, num_partitions=None, chunk_size=128):
        """
        Creates a new social data app
        :param app_name: application (or sub-application) name
        :param driver: the driver of the execution environment to use
        :param num_partitions: the preferrend number of partitions of the input files
        :param chunk_size: the preferred size of the data chunks read from the input files
        """
        self.__app_name = app_name
        self.__num_partitions = num_partitions
        self.__chunk_size = chunk_size
        self.__driver = driver
        
        self.__crawlers: List[Crawler] = []
        self.__filters: List[Filter] = []
        self.__mapper: Optional[Mapper[K, V]] = None
        self.__secondary_sort_key_function: Optional[Callable[[V], Any]] = None
        self.__reducer: Optional[Reducer[V, R]] = None
        self.__analyzer: Optional[Analyzer[K, R, A]] = None
        self.__visualizer: Optional[Visualizer[A]] = None
        self.__report_file: str = "parsoda_report.csv"
        
    def set_num_partitions(self, num_partitions: int):
        """
        Sets the number of partitions. This is overriden by the chunk size if it is set.

        Args:
            num_partitions (int): The wanted partitions number per crawler

        Returns:
            SocialDataApp: this SocialDataApp instance
        """
        self.__num_partitions = num_partitions
        return self

    def set_chunk_size(self, chunk_size: int):
        """
        Sets the data chunk size in megabytes. This parameter overrides the number of partitions.

        Args:
            chunk_size (int): The wanted partition size

        Returns:
            SocialDataApp: this SocialDataApp instance
        """
        self.__chunk_size = chunk_size
        return self
        
    def set_report_file(self, filename: str):
        """
        Sets the file name of the ParSoDA report

        Args:
            filename (str): The file name where the report will be saved

        Returns:
            SocialDataApp: this SocialDataApp instance
        """
        self.__report_file = filename
        return self

    def set_crawlers(self, crawlers: List[Crawler]):
        """Sets the list of crawlers to be used for loading data

        Args:
            crawlers (List[Crawler]): A list of Crawler objects

        Raises:
            Exception: if no crawler is given

        Returns:
            SocialDataApp: this SocialDataApp instance
        """
        if crawlers is None or len(crawlers) == 0:
            raise Exception("No crawler given")
        self.__crawlers = []
        for func in crawlers:
            self.__crawlers.append(func)
        return self

    def set_filters(self, filters: List[Filter]):
        """Sets the filters to be applied to data

        Args:
            filters (List[Filter]): the list of filters

        Raises:
            Exception: if no filter is given

        Returns:
            SocialDataApp: this SocialDataApp instance
        """
        if filters is None or len(filters) == 0:
            raise Exception("No filter given")
        self.__filters = []
        for func in filters:
            self.__filters.append(func)
        return self

    def set_mapper(self, mapper: Mapper[K, V]):
        """Sets the mapper to be used in Map-Reduce step

        Args:
            mapper (Mapper[K, V]): the mapper

        Raises:
            Exception: if no mapper is given

        Returns:
            SocialDataApp: this SocialDataApp instance
        """
        if mapper is None:
            raise Exception("No mapper given")
        self.__mapper = mapper
        return self

    def set_secondary_sort_key(self, key_function: Callable[[V], SORTABLE_KEY]):
        """Sets a key-function to be used for secondary sort step. If no key-function is set, the secondary sort will not be executed. 
        A key object returned by the specified key-function must be a sortable object, i.e. an object that can be compared to other objects of the same type.

        Args:
            key_function (Callable[[V], SORTABLE_KEY]): a callable object which maps an item to a key.

        Raises:
            Exception: if no key-function is given

        Returns:
            SocialDataApp: this SocialDataApp instance
        """
        if key_function is None:
            raise Exception("No key function given")
        self.__secondary_sort_key_function = key_function
        return self

    def set_reducer(self, reducer: Reducer[K, V, R]):
        """Sets the reducer to be used in Map-Reduce step.

        Args:
            reducer (Reducer[K, V, R]): the reducer

        Raises:
            Exception: if no reducer is given

        Returns:
            SocialDataApp: this SocialDataApp instance
        """
        if reducer is None:
            raise Exception("No reducer given")
        self.__reducer = reducer
        return self

    def set_analyzer(self, analyzer: Analyzer[K, R, A]):
        """Sets an optional analysis function.
        This could be a function that creates a new SocialDataApp instance and could use the same driver given in the current one.

        Args:
            analyzer (Analyzer[K, R, A]): the analyzer

        Raises:
            Exception: if no analyzer is given

        Returns:
            SocialDataApp: this SocialDataApp instance
        """
        if analyzer is None:
            raise Exception("No analyzer given")
        self.__analyzer = analyzer
        return self

    def set_visualizer(self, visualizer: Visualizer[A]):
        """Set an optional function for the visualization step (e.g., a function that writes results to a file)

        Args:
            visualizer (Visualizer[A]): the visualizer

        Raises:
            Exception: if no analyzer is given

        Returns:
            SocialDataApp: this SocialDataApp instance
        """
        if visualizer is None:
            raise Exception("No visualizer given")
        self.__visualizer = visualizer
        return self

    def execute(self) -> ParsodaReport:
        """Runs the application and returns a report about its execution.

        Raises:
            Exception: if some preliminary check fails (e.g. no crawlers are set) or some ParSoDA step fails during the execution.

        Returns:
            ParsodaReport: the execution report
        """
        # Check application components
        if self.__crawlers is None or len(self.__crawlers) == 0:
            raise Exception("No crawler is set")
        if self.__filters is None:
            self.__filters: List[Filter] = []
        if self.__mapper is None:
            raise Exception("No mapper is set")
        if self.__reducer is None:
            raise Exception("No reducer is set")
        
        # Optional analyzer and visualizer warnings
        if self.__analyzer is None and self.__visualizer is not None:
            print("WARNING: the visualizer is set, but analyzer is not. Visualization will not be executed in this condition!")
        else:
            if self.__analyzer is None:
                print("WARNING: No analyzer is set")
            if self.__visualizer is None:
                print("WARNING: No visualizer is set")

        # VERY IMPORTANT: de-couples all objects from "self"
        # Avoids "self" to be serialized by some execution environment (e.g., PySpark)
        driver = self.__driver
        reducer = self.__reducer
        secondary_key = self.__secondary_sort_key_function

        # Start ParSoDA workflow, initialize driver
        print(f"[ParSoDA/{self.__app_name}] initializing driver: {type(self.__driver).__name__}")
        driver.set_chunk_size(self.__chunk_size*1024*1024)
        driver.set_num_partitions(self.__num_partitions)
        driver.init_environment()

        # defines performance times variables
        crawling_time: int
        filter_time: int
        map_time: int
        split_time: int
        reduce_time: int
        analysis_time: int
        visualization_time: int

        # create a stopwatch for collecting execution times of ParSoDA phases
        stopwatch = StopWatch()

        print(f"[ParSoDA/{self.__app_name}] crawling")
        driver.crawl(self.__crawlers)
        crawling_time = stopwatch.get_and_reset()
        
        print(f"[ParSoDA/{self.__app_name}] filtering \"None\" values")
        driver.filter(_filter_none)

        # item1, item2, item3, item4, ...

        print(f"[ParSoDA/{self.__app_name}] filtering")
        for filter_func in self.__filters:
            driver.filter(filter_func.test)
        filter_time = stopwatch.get_and_reset()

        # item1, item3, item4, item7, ...

        print(f"[ParSoDA/{self.__app_name}] mapping")
        driver.flatmap(self.__mapper.map)
        map_time = stopwatch.get_and_reset()

        # (k1, v1) (k1, v2), (k2, v3) ...

        print(f"[ParSoDA/{self.__app_name}] splitting")
        driver.group_by_key()

        # k1 -> [v2, v1, v6, v5 ...], k2 -> [v8, v5, v3 ...], ... (unsorted values)

        # sort values (optional)
        if secondary_key is not None:
            print(f"[ParSoDA/{self.__app_name}] secondary sorting")
            driver.map(_sort_kvs(secondary_key))
        
        split_time = stopwatch.get_and_reset()

        print(f"[ParSoDA/{self.__app_name}] reducing")
        driver.map(_reduce(reducer))

        # k1 -> r1, k2 -> r2, k3 -> r3, ...

        print(f"[ParSoDA/{self.__app_name}] filtering \"None\" values")
        driver.filter(_filter_kv_none)
        
        # k1 -> r1, k3 -> r3, k6 -> r6, ...

        print(f"[ParSoDA/{self.__app_name}] collecting reduction results")
        reduction_result = dict(driver.get_result())
        reduce_time = stopwatch.get_and_reset()

        # reduction_result == {k1 -> r1, k3 -> r3, k6 -> r6, ...}
        
        reduction_result_length = len(reduction_result)
        print(f"[ParSoDA/{self.__app_name}] len(reduction_result)={reduction_result_length}")
        stopwatch.reset()

        print(f"[ParSoDA/{self.__app_name}] disposing driver")
        driver.dispose_environment()

        if(self.__analyzer is not None):
            print(f"[ParSoDA/{self.__app_name}] analyzing")
            analysis_result = self.__analyzer.analyze(driver, reduction_result)
            analysis_time = stopwatch.get_and_reset()
            
            if(self.__visualizer is not None):
                print(f"[ParSoDA/{self.__app_name}] visualizing")
                self.__visualizer.visualize(analysis_result)
                visualization_time = stopwatch.get_and_reset()
            else:
                print(f"[ParSoDA/{self.__app_name}] skipping visualization, as the visualizer is not set")
        else:
            print(f"[ParSoDA/{self.__app_name}] skipping analysis and visualization, as the analyzer is not set")

        print(f"[ParSoDA/{self.__app_name}] building report")

        report = ParsodaReport(
            self.__app_name,
            self.__driver,
            self.__num_partitions,
            self.__chunk_size,
            crawling_time,
            filter_time,
            map_time,
            split_time,
            reduce_time,
            analysis_time,
            visualization_time,
            reduce_result_length=reduction_result_length
        )
        print(report)
        
        print(f"[ParSoDA/{self.__app_name}] report written to \"{self.__report_file}\"")

        with open(self.__report_file, "w") as f:
            f.write(report.to_csv_line())

        return report

