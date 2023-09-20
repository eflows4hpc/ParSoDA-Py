from parsoda.model.driver.parsoda_driver import ParsodaDriver

import argparse

class ParsodaUseCaseParameters:
    def __init__(self):
        
        def type_driver(arg: str) -> ParsodaDriver:
            if arg == "pycompss":
                from parsoda.model.driver.parsoda_pycompss_driver import ParsodaPyCompssDriver
                return ParsodaPyCompssDriver()
            elif arg == "pyspark":
                from parsoda.model.driver.parsoda_pyspark_driver import ParsodaPySparkDriver
                import pyspark
                return ParsodaPySparkDriver(pyspark.SparkContext(conf=pyspark.SparkConf()))
            elif arg == "singlecore":
                from parsoda.model.driver.parsoda_singlecore_driver import ParsodaSingleCoreDriver
                return ParsodaSingleCoreDriver()
            else:
                raise Exception(f"Undefined driver \"{arg}\"")

        parser = argparse.ArgumentParser(description='Trajectory Mining application on top of PyCOMPSs')

        parser.add_argument(
            "driver",
            type=type_driver,
            help="ParSoDA driver to use. It can be: 'pycompss', 'pyspark' or 'singlecore'"
        )
        parser.add_argument(
            "--partitions", "-p",
            type=int,
            default=-1,
            help="specifies the number of data partitions."
        )
        parser.add_argument(
            "--chunk-size", "-c",
            type=int,
            default=128,
            help="specifies the size of data partitions in megabytes."
        )
        cmd_args = parser.parse_args()
        self.__driver = cmd_args.driver
        self.__chunk_size = cmd_args.chunk_size
        self.__partitions = cmd_args.partitions
        
    @property
    def driver(self)->ParsodaDriver:
        return self.__driver
    @property
    def chunk_size(self)->int:
        return self.__chunk_size
    @property
    def partitions(self)->int:
        return self.__partitions