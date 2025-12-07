"""KMeans clustering algorithm implemented in C."""

from kmeans._core import kmeans
from kmeans.estimator import KMeans

__version__ = "v0.1.0"
__all__ = ["KMeans", "kmeans"]
