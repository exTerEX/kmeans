"""Core k-means clustering functionality."""

import numpy as np

try:
    from kmeans import _kmeans  # pragma: no cover
except ImportError as e:  # pragma: no cover
    raise ImportError(
        "The _kmeans C extension could not be imported. "
        "Please ensure the package is properly installed with: pip install ."
    ) from e


def kmeans(data, k, max_iterations=100, tolerance=1e-4):
    """
    Perform k-means clustering on the given data.

    Parameters
    ----------
    data : array-like of shape (n_samples, n_features)
        The input data to cluster.
    k : int
        The number of clusters.
    max_iterations : int, optional
        Maximum number of iterations (default: 100).
    tolerance : float, optional
        Convergence tolerance (default: 1e-4).

    Returns
    -------
    centroids : ndarray of shape (k, n_features)
        The final cluster centroids.
    labels : ndarray of shape (n_samples,)
        Index of the cluster each sample belongs to.
    """
    data = np.ascontiguousarray(data, dtype=np.float64)
    if data.ndim == 1:
        data = data.reshape(-1, 1)

    centroids, labels = _kmeans.fit(
        data, int(k), int(max_iterations), float(tolerance)
    )
    return centroids, labels
