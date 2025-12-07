"""Scikit-learn compatible KMeans estimator."""

import numpy as np

from kmeans._core import kmeans

try:
    from kmeans import _kmeans  # pragma: no cover
except ImportError as e:  # pragma: no cover
    raise ImportError(
        "The _kmeans C extension could not be imported. "
        "Please ensure the package is properly installed with: pip install ."
    ) from e


class KMeans:
    """
    K-Means clustering.

    Parameters
    ----------
    n_clusters : int
        The number of clusters to form.
    max_iter : int, optional
        Maximum number of iterations (default: 100).
    tol : float, optional
        Convergence tolerance (default: 1e-4).
    """

    def __init__(self, n_clusters, max_iter=100, tol=1e-4):
        self.n_clusters = n_clusters
        self.max_iter = max_iter
        self.tol = tol
        self.centroids_ = None
        self.labels_ = None

    def fit(self, X):
        """
        Compute k-means clustering.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Training data.

        Returns
        -------
        self : KMeans
            Fitted estimator.
        """
        self.centroids_, self.labels_ = kmeans(
            X, self.n_clusters, self.max_iter, self.tol
        )
        return self

    def predict(self, X):
        """
        Predict the closest cluster for each sample.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            New data to predict.

        Returns
        -------
        labels : ndarray of shape (n_samples,)
            Index of the cluster each sample belongs to.
        """
        if self.centroids_ is None:
            raise ValueError("Model not fitted. Call fit() first.")

        X = np.ascontiguousarray(X, dtype=np.float64)
        if X.ndim == 1:
            X = X.reshape(-1, 1)

        return _kmeans.predict(
            X, np.ascontiguousarray(self.centroids_, dtype=np.float64)
        )

    def fit_predict(self, X):
        """
        Compute clustering and return cluster labels.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Training data.

        Returns
        -------
        labels : ndarray of shape (n_samples,)
            Index of the cluster each sample belongs to.
        """
        self.fit(X)
        return self.labels_
