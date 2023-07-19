# ParSoDA-Python
This project is a porting of the ParSoDA java library to the python environment. 
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


