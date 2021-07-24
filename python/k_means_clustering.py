"""
k_means_clustering.py

Python interface to c library to cluster observations.

Copyright 2021 Andreas Sagen

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from random import randint
import sys
from ctypes import *
from typing import *

from numpy import ndarray
from numpy import issubdtype
from numpy import number, integer
from pandas import DataFrame

try:
    lib = CDLL(f"build/kmeans_{sys.platform}.so")
except BaseException:
    print(f"OS {sys.platform} not recognized")


class observation(Structure):
    _fields_ = [
        ("x", c_double),
        ("y", c_double),
        ("group", c_size_t),
    ]


class cluster(Structure):
    _fields_ = [
        ("x", c_double),
        ("y", c_double),
        ("count", c_size_t)
    ]


lib.k_means.restype = POINTER(cluster)


def k_means(observations: DataFrame, k: Optional[integer] = 5) -> DataFrame:

    if not isinstance(observations, DataFrame):
        raise TypeError("Observations must be a pandas.Dataframe.")

    if observations.shape[-1] != 2:
        raise ValueError(
            "Observation doesn't have the correct number of columns.")

    # Expected dtypes of the observations DataFrame
    expected = (number, number)

    # Check if the dtypes of observations corresponds to the expectation
    result = map(issubdtype, observations.dtypes, expected)

    if not all(result):
        raise ValueError("Observations can only contain numbers.")

    # Unpack values
    x = observations.iloc[:, 0].to_list()
    y = observations.iloc[:, 1].to_list()

    # Create a Python list of observations
    pyObservations = map(observation, x, y)

    # Convert the Python list into a c-array
    cObservations = (observation * len(x))(*pyObservations)

    # Get c-array of cluster
    cClusters = lib.k_means(cObservations, c_size_t(len(x)), c_size_t(k))

    # Convert c-array of clusters into a python list
    pyClusters = [cClusters[index] for index in range(k)]

    # Split clusters
    x, y, count = [], [], []
    for obj in pyClusters:
        x.append(obj.x)
        y.append(obj.y)
        count.append(obj.count)

    # Pack into DataFrame and return
    return DataFrame(
        {"x": x, "y": y, "count": count},
        columns=["x", "y", "count"])


if __name__ == "__main__":
    import random
    import numpy

    random.seed(1234)

    x, y = [], []

    for index in range(0, 100):
        radius = 10 * random.random()
        angle = 2 * numpy.pi * random.random()

        x.append(radius * numpy.cos(angle))
        y.append(radius * numpy.sin(angle))

    df = DataFrame({"x": x, "y": y})

    print(k_means(df, 5))
