Python API Reference
====================

.. automodule:: kmeans
   :members:
   :undoc-members:
   :show-inheritance:

Functional API
--------------

.. autofunction:: kmeans.kmeans

Object-Oriented API
-------------------

KMeans Class
~~~~~~~~~~~~

.. autoclass:: kmeans.KMeans
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__

   .. automethod:: __init__
   .. automethod:: fit
   .. automethod:: predict
   .. automethod:: fit_predict

Attributes
^^^^^^^^^^

After calling :meth:`fit`, the following attributes are available:

.. py:attribute:: centroids_

   :type: numpy.ndarray of shape (n_clusters, n_features)

   Coordinates of cluster centers.

.. py:attribute:: labels_

   :type: numpy.ndarray of shape (n_samples,)

   Labels of each point indicating cluster assignment.

C Extension Module
------------------

.. note::
   The ``_kmeans`` module is a low-level C extension. Most users should use
   the high-level Python API instead.

.. py:module:: kmeans._kmeans

.. py:function:: fit(data, k, max_iterations, tolerance)

   Low-level k-means fitting function.

   :param numpy.ndarray data: Input data array (n_samples, n_features)
   :param int k: Number of clusters
   :param int max_iterations: Maximum iterations
   :param float tolerance: Convergence tolerance
   :return: Tuple of (centroids, labels)
   :rtype: tuple[numpy.ndarray, numpy.ndarray]

.. py:function:: predict(data, centroids)

   Predict cluster labels for data points.

   :param numpy.ndarray data: Input data array (n_samples, n_features)
   :param numpy.ndarray centroids: Cluster centroids (k, n_features)
   :return: Cluster labels
   :rtype: numpy.ndarray

Examples
--------

See :doc:`examples` for more usage examples.