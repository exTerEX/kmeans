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
import ctypes
import sys
from typing import List

import numpy

try:
    lib = ctypes.CDLL(f"build/kmeans_{sys.platform}.so")
except BaseException:
    print(f"OS {sys.platform} not recognized")


class observation(ctypes.Structure):
    _fields_ = [
        ("x", ctypes.c_double),
        ("y", ctypes.c_double),
        ("group", ctypes.c_int),
    ]


class cluster(ctypes.Structure):
    _fields_ = [
        ("x", ctypes.c_double),
        ("y", ctypes.c_double),
        ("count", ctypes.c_size_t)
    ]


# TODO: return and accept numpy arrays?
lib.k_means.restype = ctypes.POINTER(cluster)  # None


def k_means(observations: numpy.ndarray, k: int) -> List[cluster]:
    """Generate a K-means cluster from observations.

    Parameters
    ----------
    observations : (N, 3) array_like
        Observations in format (x, y, group).
    k : int
        Number of clusters to partition observations into.

    Returns
    -------
    List[cluster]
        [description]
    """

    o = []
    for index, (x, y, group) in enumerate(observations):
        x, y, group = float(x), float(y), int(group)

        o.append(
            observation(
                ctypes.c_double(x),
                ctypes.c_double(y),
                ctypes.c_int(group)
            )
        )

    return lib.k_means(
        ctypes.Array(o),
        ctypes.ctypes.c_size_t(len(observations)),
        ctypes.c_int(k)
    )


arr = numpy.zeros([100, 3], dtype=numpy.float)

k_means(arr, 5)
