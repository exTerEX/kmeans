from ctypes import *
from typing import *

from numpy import array, cos, ndarray, pi, random, sin, zeros, tan

try:
    lib = CDLL(f"./libkmeans.so")
except Exception as E:
    print(f"Cannot load DLL")
    print(E)


class observation_2d(Structure):
    _fields_ = [("x", c_double), ("y", c_double), ("group", c_size_t)]


class observation_3d(Structure):
    _fields_ = [("x", c_double), ("y", c_double), ("z", c_double), ("group", c_size_t)]


class cluster_2d(Structure):
    _fields_ = [("x", c_double), ("y", c_double), ("count", c_size_t)]


class cluster_3d(Structure):
    _fields_ = [("x", c_double), ("y", c_double), ("z", c_double), ("count", c_size_t)]


lib.k_means_2d.restype = POINTER(cluster_2d)


def k_means_2d(observations: ndarray, k: Optional[int] = 5) -> Tuple[ndarray, ndarray]:
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
    >>> center, count = k_means_2d(observations, k=2)
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

    # Find observation_2d length
    n = observations.shape[-1]

    # Create a Python list of observations
    py_observations_list = map(observation_2d, *observations)

    # Convert the Python list into a c-array
    c_observations_array = (observation_2d * n)(*py_observations_list)

    # Get c-array of cluster_2d
    c_clusters_array = lib.k_means_2d(
        c_observations_array, c_size_t(n), c_size_t(k))

    # Convert c-array of clusters into a python list
    py_clusters_list = [c_clusters_array[index] for index in range(k)]

    # Split clusters
    center = zeros([k, 2], dtype=observations.dtype)
    count = zeros(k, dtype=int)

    for index, cluster_object in enumerate(py_clusters_list):
        center[index][0] = cluster_object.x
        center[index][1] = cluster_object.y
        count[index] = cluster_object.count

    # Pack into DataFrame and return
    return (center, count)


lib.k_means_3d.restype = POINTER(cluster_3d)


def k_means_3d(observations: ndarray, k: Optional[int] = 5) -> Tuple[ndarray, ndarray]:
    """Partition observations into k clusters.

    Parameters
    ----------
    observations : ndarray, `shape (N, 3)`
        An array of observations (x, y) to be clustered.

        Data should be provided as: `[(x, y, z), (x, y, z), (x, y, z), ...]`

    k : int, optional
        Amount of clusters to partition observations into, by default 5

    Returns
    -------
    center : ndarray, `shape (k, 3)`
        An array of positions to center of each cluster.

    count : ndarray, `shape (k, )`
        Array of counts of datapoints closest to the center of its cluster.

    Examples
    -------
    >>> observations = [[6, 1, 3], [-4, -4, -4], [1, -7, 7], [9, -2, 1], [6, -6, 6]]
    >>> center, count = k_means_3d(observations, k=2)
    >>> center
    [[ -0.35830777  -7.41219447 201.90265473]
     [  1.83808572  -5.86460671 -28.00696338]
     [ -0.81562641  -1.20418037   1.60364838]]
    >>> count
    [2, 3]
    """
    if not isinstance(observations, ndarray):
        raise TypeError("Observations must be a ndarray.")

    # Fix orientation on data
    if observations.shape[-1] == 3:
        observations = observations.T
    else:
        raise ValueError("Provided array should contain ((x, y, z), ) observations.")

    # Find observation_3d length
    n = observations.shape[-1]

    # Create a Python list of observations
    py_observations_list = map(observation_3d, *observations)

    # Convert the Python list into a c-array
    c_observations_array = (observation_3d * n)(*py_observations_list)

    # Get c-array of cluster_2d
    c_clusters_array = lib.k_means_3d(c_observations_array, c_size_t(n), c_size_t(k))

    # Convert c-array of clusters into a python list
    py_clusters_list = [c_clusters_array[index] for index in range(k)]

    # Split clusters
    center = zeros([k, 3], dtype=observations.dtype)
    count = zeros(k, dtype=int)

    for index, cluster_object in enumerate(py_clusters_list):
        center[index][0] = cluster_object.x
        center[index][1] = cluster_object.y
        center[index][2] = cluster_object.z
        count[index] = cluster_object.count

    # Pack into DataFrame and return
    return (center, count)


def kmeans(observations: ndarray, k: Optional[int] = 5) -> Tuple[ndarray, ndarray]:
    """Partition observations into k clusters.

    Parameters
    ----------
    observations : ndarray, `shape (N, 2)` or `shape (N, 3)`
        An array of observations (x, y) to be clustered.

        Data should be provided as:
        `[(x, y), (x, y), (x, y), ...]`
        or
        `[(x, y, z), (x, y, z), (x, y, z), ...]`

    k : int, optional
        Amount of clusters to partition observations into, by default 5

    Returns
    -------
    center : ndarray, `shape (k, 2)` or `shape (k, 3)`
        An array of positions to center of each cluster.

    count : ndarray, `shape (k, )`
        Array of counts of datapoints closest to the center of its cluster.

    Examples
    -------
    >>> observations = [[6, 1], [-4, -4], [1, -7], [9, -2], [6, -6]]
    >>> center, count = k_means_2d(observations, k=2)
    >>> center
    [[-4, -4
       5, -3]]
    >>> count
    [1, 4]
    """

    if not isinstance(observations, ndarray):
        raise TypeError("Observations must be a ndarray.")

    if observations.shape[-1] == 3:
        return k_means_3d(observations, k)
    elif observations.shape[-1] == 2:
        return k_means_2d(observations, k)
    else:
        pass


if __name__ == "__main__":
    random.seed(1234)

    rand_list = random.random(100)

    x = 10 * rand_list * cos(2 * pi * rand_list)
    y = 10 * rand_list * sin(2 * pi * rand_list)
    z = 10 * rand_list * tan(2 * pi * rand_list)

    df = array([x, y, z]).T

    print(f"Observations:\n{df[0:5]}\n...\n\nshape {len(df), len(df[0])}\n")

    centers, count = kmeans(df, 3)

    print(f"Centers:\n{centers}\n")
    print(f"Count:\n{count}")

    observations = [[6, 1], [-4, -4], [1, -7], [9, -2], [6, -6]]
    center, count = k_means_2d(array(observations), k=2)

    print(f"Centers:\n{centers}\n")
    print(f"Count:\n{count}")
