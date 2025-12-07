C API Reference
===============

This page documents the C implementation details for developers who want to
understand or extend the underlying algorithm.

.. note::
   The C extension is implemented in ``src/kmeans/_kmeans.c``. 
   This documentation describes the algorithm and function signatures.

Algorithm Overview
------------------

The k-means implementation uses the following approach:

1. **Initialization**: K-means++ algorithm for better initial centroids
2. **Assignment**: Assign each point to nearest centroid
3. **Update**: Recalculate centroids as mean of assigned points
4. **Convergence**: Repeat until centroids stop moving significantly

Core Functions
--------------

Distance Calculation
~~~~~~~~~~~~~~~~~~~~

.. code-block:: c

   static double squared_distance(const double *a, const double *b, int dims)

Calculate squared Euclidean distance between two points.

:param a: First point coordinates
:param b: Second point coordinates  
:param dims: Number of dimensions
:return: Squared distance

Find Nearest Centroid
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c

   static int find_nearest_centroid(const double *point, 
                                     const double *centroids,
                                     int k, int dims)

Find the index of the nearest centroid for a given point.

:param point: Data point coordinates
:param centroids: Array of all centroid coordinates
:param k: Number of clusters
:param dims: Number of dimensions
:return: Index of nearest centroid (0 to k-1)

K-means++ Initialization
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c

   static void init_centroids_kmeanspp(const double *data, 
                                        int n_samples, int dims,
                                        int k, double *centroids)

Initialize centroids using the k-means++ algorithm.

The k-means++ initialization chooses initial cluster centers that are
far apart, leading to better and faster convergence.

:param data: Input data array
:param n_samples: Number of data points
:param dims: Number of dimensions
:param k: Number of clusters
:param centroids: Output array for centroid coordinates

**Algorithm:**

1. Choose first centroid uniformly at random
2. For each remaining centroid:
   
   a. Calculate distance to nearest existing centroid for each point
   b. Choose new centroid with probability proportional to squared distance

Main K-means Algorithm
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c

   static int kmeans_core(const double *data, int n_samples, int dims, 
                          int k, int max_iter, double tol, 
                          double *centroids, int *labels)

Main k-means clustering algorithm.

:param data: Input data array (row-major, n_samples × dims)
:param n_samples: Number of data points
:param dims: Number of dimensions
:param k: Number of clusters
:param max_iter: Maximum number of iterations
:param tol: Convergence tolerance
:param centroids: Output array for final centroids
:param labels: Output array for cluster assignments
:return: 0 on success, -1 on memory allocation failure

**Convergence:**

The algorithm stops when the maximum centroid shift is less than ``tol``,
or when ``max_iter`` iterations have been reached.

Python Binding Functions
-------------------------

.. code-block:: c

   static PyObject *py_fit(PyObject *self, PyObject *args)

Python wrapper for the fit operation. Accepts NumPy arrays and returns 
tuple of (centroids, labels).

.. code-block:: c

   static PyObject *py_predict(PyObject *self, PyObject *args)

Python wrapper for the predict operation. Assigns new data points to 
existing centroids.

Memory Management
-----------------

The C implementation uses dynamic memory allocation for:

* Temporary centroid calculations
* Cluster point counts
* Distance calculations in k-means++

All allocations are freed before function return. Error checking ensures
proper cleanup on allocation failures.

Performance Considerations
--------------------------

Optimization Techniques
~~~~~~~~~~~~~~~~~~~~~~~

1. **Memory Layout**: Row-major array layout for cache efficiency
2. **Squared Distance**: Avoid expensive sqrt() in distance calculations
3. **Early Termination**: Stop when convergence tolerance is reached
4. **K-means++**: Better initialization reduces iterations needed

Complexity
~~~~~~~~~~

* **Time**: O(n × k × d × i) where:
  
  * n = number of samples
  * k = number of clusters
  * d = number of dimensions
  * i = number of iterations

* **Space**: O(n + k × d)

Building the C Extension
-------------------------

The C extension is built using CMake:

.. code-block:: cmake

   # From CMakeLists.txt
   python_add_library(_kmeans MODULE
       src/kmeans/_kmeans.c
       WITH_SOABI
   )

   target_include_directories(_kmeans PRIVATE
       ${Python_NumPy_INCLUDE_DIRS}
       ${CMAKE_SOURCE_DIR}/include
   )

   target_link_libraries(_kmeans PRIVATE Python::NumPy)

Source Code Location
--------------------

The complete C implementation can be found in:

* ``src/kmeans/_kmeans.c`` - Main implementation file
* ``CMakeLists.txt`` - Build configuration

See the source files directly for the most up-to-date implementation details.