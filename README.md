# ParSoDA-Py
This project is a redesign of the ParSoDA java library for the Python environment. 
ParSoDA has been extended to support multiple execution runtimes. Specifically, according to the bridge design pattern, we defined the ParsodaDriver interface (i.e., the implementor of the bridge pattern) that allows a developer to implement adapters for different execution systems. A valid instance of ParsodaDriver must invoke some function that exploits some parallel pattern, such as Map, Filter, ReduceByKey and SortByKey. The SocialDataApp class is the abstraction of the bridge pattern and is designed to use these parallel patterns efficiently for running ParSoDA applications. It is worth noting that the execution flow of an application remains unchanged even by changing the execution runtime, which allows to run ParSoDA applications on different execution runtimes without modifying their code at all.

# Dependencies
The ParSoDA library strictly requires Python 3.8 or above.
At least one of the following libraries is required in order to execute ParSoDA applications on a distributed system:

  - PyCOMPSs 2.10 or above version;
  - PySpark 3.2 or above version.

For executing ParSoDA sample applications, i.e. Trajectory Mining and Emoji Polarization, included in this repository, the following Python libraries are required::

    emoji>=1.7.0,<2
    fastkml>=0.12,<1
    geopy>=2.2.0,<3
    shapely>=2.0.1,<3
 
The ParSoDA package contains a file “requirements.txt” which can be used with pip to install the application requirements, executing the following command in the root directory of ParSoDA::

    python3 -m pip install -r requirements.txt 

# Installing ParSoDA through pip
ParSoDA can be installed by pip through the setup.py script. You just need to change current directory to the root of this repository

    cd <ParSoDA repo root directory>

and run

    pip3 install .

# ParSoDA on top of PyCOMPSs
For using the ParSoDA library on top of PyCOMPSs, it is required to import and instantiate the ParsodaPyCompssDriver class, as in the following Trajectory Mining example:

    driver = ParsodaPyCompssDriver()
    
    app = SocialDataApp("Trajectory Mining", driver, num_partitions=args.partitions, chunk_size=args.chunk_size)

    app.set_crawlers([
        LocalFileCrawler('/root/dataset/FlickrRome2017.json', FlickrParser())
        LocalFileCrawler('/root/dataset/TwitterRome2017.json', TwitterParser())
    ])
    app.set_filters([
        IsInRoI("./resources/input/RomeRoIs.kml")
    ])
    app.set_mapper(FindPoI("./resources/input/RomeRoIs.kml"))
    app.set_secondary_sort_key(lambda x: x[0])
    app.set_reducer(ReduceByTrajectories(3))
    app.set_analyzer(GapBIDE(1, 0, 10))
    app.set_visualizer(
        SortGapBIDE(
            "./resources/output/trajectory_mining.txt", 
            'support', 
            mode='descending', 
            min_length=3
        )
    )

    app.execute()

# Running an application
For running an application, it is recommended to see the instructions of the execution environment used.
For example, for running an application that uses the ParsodaPyCompssDriver, it is required to run its main program through the "runcompss" command, as specified in the documentation of PyCOMPSs.

# Unit and integration tests
The project uses the "unittest" Python package in order to run unit and integration tests. Integration tests are very useful in order to validate the correctness of the ParSoDA workflow after bug fixes, introduction of new features and, overall for testing compatibility with new dependencies and runtimes versions (e.g., PySpark and PyCOMPSs).

For running unit and integration test, use the following command:

    python3 -m unittest -v

# Performace tests
In order to evaluate the performance of ParSoDA on top of runtime environments, the projects provide some script for running performance tests, obtaining latency and speed-up.
A performance test is batch of runs of some spacified use-cases.

For running the performance test use the following command from the root of this repository:

    PYTHONPATH=. python3 test/performance.py

For defining a new performance test, follow the next steps:

1. define a use-case in "test/usecase" directory;
2. if it is needed, define a new runtime command in "test/runtime";
3. modify the parameters at the head of the "test/performance.py" script to be aligned to your test needs.

## Defining a new use case
A use case is basically the definintion of an application that runs with well defined parameters (e.g. a specific input dataset, a specific Regions of Interest file, a specific GapBIDE minimum support value, etc.). 

The parameters of a use case concern only the execution environment and data partitioning.

For defining a new use case, the developer must follow the next steps:

1. create a new runnable script in "test/usecase" directory;
2.  import the test.usecase.parsoda_usecase_parameters.ParsodaUseCaseParameters;
3.  load test parameters by simply creating a new ParsodaUseCaseParameters object and accessing its properties;
4.  create and run the lication with hard-coded algorithm input parameters:

        test = ParsodaUseCaseParameters()
        app = SocialDataApp("App Name", test.driver, test.partitions, test.chunk_size)
        app.set_crawlers([DistributedFileCrawler("hard-coded/path/to/a_dataset", TwitterParser())])
        ...

## Defining a new test runtime
A test runtime allows to define a specific configuration for an underlying ParSoDA runtime (e.g. a specific configuration of the COMPSs environment), just for performace testing purposes.

If you want test the ParSoDA libray, most likely you want to define your own test runtime and run one or more of the already defined use-cases.

For defining a new test runtime you must follow these steps:

1. create a .py file in "test/runtime" or append your runtime definition to one of the already existing ones (possibily except the "test_runtime.py" file, which defines the TestRuntime abstract type);
2. define your runtime as a class with just one "run(self, app, chunk_size, cores, log_file_path)" method. The class must extend the test.runtime.test_runtime.TestRuntime as in the next example:

        class PyCompssScalabTestRuntime(TestRuntime):    
        def run(self, app, chunk_size, cores, log_file_path) -> int:
            exit_code = os.system(
                f"runcompss --python_interpreter=python3 "
                f"--resources=./test/config/pycompss-scalab-docker/resources.xml "
                f"--project=./test/config/pycompss-scalab-docker/project-{cores}cores.xml "
                f"--jvm_workers_opts=\"-Xmx20g\" "
                f"{app} pycompss --chunk-size {chunk_size}"
                f" > {log_file_path}"
            )
            return exit_code

Note that the run method, just invokes a shell command submitting the "app" (that is the selected use-case) and setting up the environment with the given parameters.

# Docker containers
For testing ParSoDA a Docker container can be created.
In order to build the Docker image run the following command in the root of this repository:

    docker build . -t "<your image name>"

The image comes out with many installed packages and tools, including the following:
-   "pyspark" and "pycompss" pip packages
-   Gradle and OpenJDK 1.8
-   Git

NB: PyCOMPSs is alredy configured and usable for creating a cluster of containers.

NB: pyspark package could not be used for creating a cluster of containers, it requires some additional configuration or a new image.

# Create a test container
You can create the testing container by setting up the following docker stack:

    version: '3'
    services:
        app:
            image: <your image name>
            restart: unless-stopped

# Create a container for supporting the development of ParSoDA-Py
If you want support the ParSoDA development you could create the development container by mounting the directory of the parsoda project in the /parsoda directory, with a Docker stack similar to the following:

    version: '3'
    services:
        app:
            image: <your image name>
            volumes:
                - "/path/to/parsoda_project:/parsoda"
                - "/path/to/your/id_rsa:/root/.ssh/id_rsa" # access a remote fork of ParSoDA-Py
            restart: unless-stopped

            


