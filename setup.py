import os, sys
from setuptools import find_packages, setup

with open("README.md", "r") as f:
    readme = f.read()

with open("requirements.txt", "r") as f:
    requirements = [req.strip() for req in f.readlines()]
    
setup(
    name = "ParSoDA",
    version = "1.1.0",
    author = "", #TODOS
    author_email = "", #TODO
    description = ("ParSoDA: Parallel Social Data Analytics library, running on multiple environments"),
    license = "", #TODO
    keywords =  "social data analysis scalability parallel big-data social-media social-networks distributed-computing"
                "media networks distributed computing trajectory mining pattern roi region of interest point of interest",
    url = "https://github.com/eflows4hpc/parsoda",
    packages=find_packages(where='.'),
    long_description=readme,
    python_requires=">=3.8.0",
    install_requires=requirements,
    classifiers=[ #TODO
        #"Development Status :: 3 - Alpha",
        "Topic :: Distributed Computing", 
        #"License :: OSI Approved :: BSD License",
    ],
)