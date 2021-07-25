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

import sys
from ctypes import *
from typing import *

import numpy
from numpy import ndarray

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


def k_means(observations: ndarray, k: Optional[int] = 5) -> Tuple[ndarray, ndarray]:
    """Partition observations into k clusters.

    Parameters
    ----------
    observations : ndarray, `shape (N, 2)`
        An array of observations (x, y) to be clustered.

        Data should be provided as: `[(x, y), (x, y), (x, y), ...]`

    k : int, optional
        Amount of clusters to partition observations into, by default 5

    Returns
    -------
    center : ndarray, `shape (k, 2)`
        An array of positions to center of each cluster.

    count : ndarray, `shape (k, )`
        Array of counts of datapoints closest to the center of its cluster.

    Examples
    -------
    >>> observations = [[6, 1], [-4, -4], [1, -7], [9, -2], [6, -6]]
    >>> center, count = k_means(observations, k=2)
    >>> center
    [[-4, -4
       5, -3]]
    >>> count
    [1, 4]
    """
    if not isinstance(observations, ndarray):
        raise TypeError("Observations must be a ndarray.")

    # Fix orientation on data
    if observations.shape[-1] == 2:
        observations = observations.T
    else:
        raise ValueError("Provided array should contain ((x, y), ) observations.")

    # Find observation length
    n = observations.shape[-1]

    # Create a Python list of observations
    py_observations_list = map(observation, *observations)

    # Convert the Python list into a c-array
    c_observations_array = (observation * n)(*py_observations_list)

    # Get c-array of cluster
    c_clusters_array = lib.k_means(
        c_observations_array, c_size_t(n), c_size_t(k))

    # Convert c-array of clusters into a python list
    py_clusters_list = [c_clusters_array[index] for index in range(k)]

    # Split clusters
    center = numpy.zeros([k, 2], dtype=observations.dtype)
    count = numpy.zeros(k, dtype=int)

    for index, cluster_object in enumerate(py_clusters_list):
        center[index][0] = cluster_object.x
        center[index][1] = cluster_object.y
        count[index] = cluster_object.count

    # Pack into DataFrame and return
    return (center, count)


if __name__ == "__main__":
    numpy.random.seed(1234)

    rand_list = numpy.random.random(100)

    x = 10 * rand_list * numpy.cos(2 * numpy.pi * rand_list)
    y = 10 * rand_list * numpy.sin(2 * numpy.pi * rand_list)

    df = numpy.array([x, y]).T

    print(f"Observations:\n{df[0:5]}\n...\n\nshape {len(df), len(df[0])}\n")

    centers, count = k_means(df, 7)

    print(f"Centers:\n{centers}\n")
    print(f"Count:\n{count}")
