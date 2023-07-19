import os, sys
from pathlib import Path
from setuptools import find_packages, setup

def text_from_file(file_path: str or Path):
    with open(file_path, "r") as f:
        return f.read()
    
def list_from_file(file_path: str or Path):
    with open(file_path, "r") as f:
        return [line.strip() for line in f.readlines()]
    
setup(
    name = "ParSoDA",
    version = "1.1.1a",
    author = "Loris Belcastro, Salvatore Giampà, Fabrizio Marozzo, Domenico Talia, Paolo Trunfio",
    author_email = "belcastro@dtoklab.com, giampa@dtoklab.com, marozzo@dtoklab.com, talia@dtoklab.com, trunfio@dtoklab.com",
    description = ("ParSoDA: a Parallel Social Data Analytics library"),
    keywords =  "social,data,analysis,scalability,parallel,big data,social media,social networks,distributed computing,"
                "media,networks,distributed,computing,trajectory,mining,pattern,roi,region of interest,point of interest",
    url = "https://github.com/eflows4hpc/parsoda",
    packages=find_packages(where='.'),
    python_requires=">=3.8.0",
    install_requires=list_from_file("requirements.txt"),
    long_description=text_from_file("README.md"),
    long_description_content_type='text/markdown',
    license_files = ("LICENSE"),
    license = "GNU General Public License v3 (GPLv3)",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Distributed Computing",
    ],
)