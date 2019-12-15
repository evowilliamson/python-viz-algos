#!/usr/bin/env python

from setuptools import setup, find_packages

with open("README.md") as f:
    long_desc = f.read()

setup(name="py-viz-algs",
      version=0.1,
      description="A set of algorithms and data structures",
      long_description=long_desc,
      long_description_content_type="text/markdown", 
      keywords = "data structures algorithms graphs directed graphs acyclic",
      author="Evo Williamson",
      author_email="evowilliamson@gmail.com",
      license="GNU General Public License, version 2",
      url="https://github.com/evowilliamson/py-viz-algs",
      packages=find_packages(),
      install_requires=[
          "graphviz",
      ],
      test_suite="tests",
      classifiers=[
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Topic :: Software Development",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Operating System :: OS Independent"
        ,
      ]
     )
