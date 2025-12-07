#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <numpy/arrayobject.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <float.h>
#include <time.h>

// Calculate squared Euclidean distance between two points
static double squared_distance(const double *a, const double *b, int dims)
{
  double dist = 0.0;
  for (int i = 0; i < dims; i++)
  {
    double diff = a[i] - b[i];
    dist += diff * diff;
  }
  return dist;
}

// Find the nearest centroid for a data point
static int find_nearest_centroid(const double *point, const double *centroids, int k, int dims)
{
  int nearest = 0;
  double min_dist = DBL_MAX;

  for (int i = 0; i < k; i++)
  {
    double dist = squared_distance(point, centroids + i * dims, dims);
    if (dist < min_dist)
    {
      min_dist = dist;
      nearest = i;
    }
  }
  return nearest;
}

// Initialize centroids using k-means++ algorithm
static void init_centroids_kmeanspp(const double *data, int n_samples, int dims, int k,
                                    double *centroids)
{
  double *distances = (double *) malloc(n_samples * sizeof(double));

  // Choose first centroid randomly
  srand((unsigned int) time(NULL));
  int first_idx = rand() % n_samples;
  memcpy(centroids, data + first_idx * dims, dims * sizeof(double));

  // Choose remaining centroids
  for (int c = 1; c < k; c++)
  {
    double total_dist = 0.0;

    // Calculate distance to nearest centroid for each point
    for (int i = 0; i < n_samples; i++)
    {
      double min_dist = DBL_MAX;
      for (int j = 0; j < c; j++)
      {
        double dist = squared_distance(data + i * dims, centroids + j * dims, dims);
        if (dist < min_dist)
        {
          min_dist = dist;
        }
      }
      distances[i] = min_dist;
      total_dist += min_dist;
    }

    // Choose next centroid with probability proportional to distance
    double threshold = ((double) rand() / RAND_MAX) * total_dist;
    double cumsum = 0.0;
    int chosen = n_samples - 1;

    for (int i = 0; i < n_samples; i++)
    {
      cumsum += distances[i];
      if (cumsum >= threshold)
      {
        chosen = i;
        break;
      }
    }

    memcpy(centroids + c * dims, data + chosen * dims, dims * sizeof(double));
  }

  free(distances);
}

// Main k-means algorithm
static int kmeans_core(const double *data, int n_samples, int dims, int k, int max_iter, double tol,
                       double *centroids, int *labels)
{
  double *new_centroids = (double *) calloc(k * dims, sizeof(double));
  int *counts = (int *) calloc(k, sizeof(int));

  if (!new_centroids || !counts)
  {
    free(new_centroids);
    free(counts);
    return -1;
  }

  // Initialize centroids using k-means++
  init_centroids_kmeanspp(data, n_samples, dims, k, centroids);

  for (int iter = 0; iter < max_iter; iter++)
  {
    // Reset accumulators
    memset(new_centroids, 0, k * dims * sizeof(double));
    memset(counts, 0, k * sizeof(int));

    // Assign points to nearest centroid
    for (int i = 0; i < n_samples; i++)
    {
      int nearest = find_nearest_centroid(data + i * dims, centroids, k, dims);
      labels[i] = nearest;
      counts[nearest]++;

      for (int d = 0; d < dims; d++)
      {
        new_centroids[nearest * dims + d] += data[i * dims + d];
      }
    }

    // Update centroids
    double max_shift = 0.0;
    for (int c = 0; c < k; c++)
    {
      if (counts[c] > 0)
      {
        for (int d = 0; d < dims; d++)
        {
          new_centroids[c * dims + d] /= counts[c];
        }
      }

      double shift = squared_distance(centroids + c * dims, new_centroids + c * dims, dims);
      if (shift > max_shift)
      {
        max_shift = shift;
      }
    }

    memcpy(centroids, new_centroids, k * dims * sizeof(double));

    // Check convergence
    if (sqrt(max_shift) < tol)
    {
      break;
    }
  }

  free(new_centroids);
  free(counts);
  return 0;
}

// Python wrapper for fit function
static PyObject *py_fit(PyObject *self, PyObject *args)
{
  PyArrayObject *data_array;
  int k, max_iter;
  double tol;

  if (!PyArg_ParseTuple(args, "O!iid", &PyArray_Type, &data_array, &k, &max_iter, &tol))
  {
    return NULL;
  }

  // Validate input
  if (PyArray_NDIM(data_array) != 2)
  {
    PyErr_SetString(PyExc_ValueError, "Input data must be 2-dimensional");
    return NULL;
  }

  if (PyArray_TYPE(data_array) != NPY_FLOAT64)
  {
    PyErr_SetString(PyExc_TypeError, "Input data must be float64");
    return NULL;
  }

  int n_samples = (int) PyArray_DIM(data_array, 0);
  int dims = (int) PyArray_DIM(data_array, 1);

  if (k <= 0 || k > n_samples)
  {
    PyErr_SetString(PyExc_ValueError, "k must be between 1 and n_samples");
    return NULL;
  }

  // Create output arrays
  npy_intp centroid_dims[2] = {k, dims};
  npy_intp label_dims[1] = {n_samples};

  PyArrayObject *centroids = (PyArrayObject *) PyArray_SimpleNew(2, centroid_dims, NPY_FLOAT64);
  PyArrayObject *labels = (PyArrayObject *) PyArray_SimpleNew(1, label_dims, NPY_INT32);

  if (!centroids || !labels)
  {
    Py_XDECREF(centroids);
    Py_XDECREF(labels);
    return PyErr_NoMemory();
  }

  // Run k-means
  const double *data = (const double *) PyArray_DATA(data_array);
  double *centroids_data = (double *) PyArray_DATA(centroids);
  int *labels_data = (int *) PyArray_DATA(labels);

  int result = kmeans_core(data, n_samples, dims, k, max_iter, tol, centroids_data, labels_data);

  if (result != 0)
  {
    Py_DECREF(centroids);
    Py_DECREF(labels);
    PyErr_SetString(PyExc_MemoryError, "Failed to allocate memory");
    return NULL;
  }

  return Py_BuildValue("(OO)", centroids, labels);
}

// Python wrapper for predict function
static PyObject *py_predict(PyObject *self, PyObject *args)
{
  PyArrayObject *data_array, *centroids_array;

  if (!PyArg_ParseTuple(args, "O!O!", &PyArray_Type, &data_array, &PyArray_Type, &centroids_array))
  {
    return NULL;
  }

  if (PyArray_NDIM(data_array) != 2 || PyArray_NDIM(centroids_array) != 2)
  {
    PyErr_SetString(PyExc_ValueError, "Input arrays must be 2-dimensional");
    return NULL;
  }

  int n_samples = (int) PyArray_DIM(data_array, 0);
  int dims = (int) PyArray_DIM(data_array, 1);
  int k = (int) PyArray_DIM(centroids_array, 0);

  if ((int) PyArray_DIM(centroids_array, 1) != dims)
  {
    PyErr_SetString(PyExc_ValueError, "Data and centroids must have same dimensions");
    return NULL;
  }

  npy_intp label_dims[1] = {n_samples};
  PyArrayObject *labels = (PyArrayObject *) PyArray_SimpleNew(1, label_dims, NPY_INT32);

  if (!labels)
  {
    return PyErr_NoMemory();
  }

  const double *data = (const double *) PyArray_DATA(data_array);
  const double *centroids = (const double *) PyArray_DATA(centroids_array);
  int *labels_data = (int *) PyArray_DATA(labels);

  for (int i = 0; i < n_samples; i++)
  {
    labels_data[i] = find_nearest_centroid(data + i * dims, centroids, k, dims);
  }

  return (PyObject *) labels;
}

// Method definitions
static PyMethodDef kmeans_methods[] = {
  {"fit", py_fit, METH_VARARGS, "Fit k-means model to data"},
  {"predict", py_predict, METH_VARARGS, "Predict cluster labels for data"},
  {NULL, NULL, 0, NULL}};

// Module definition
static struct PyModuleDef kmeans_module = {PyModuleDef_HEAD_INIT, "_kmeans",
                                           "K-means clustering C extension", -1, kmeans_methods};

// Module initialization
PyMODINIT_FUNC PyInit__kmeans(void)
{
  import_array();
  return PyModule_Create(&kmeans_module);
}
