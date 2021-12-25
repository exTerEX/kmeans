#include <stdlib.h>

typedef struct observation_2d {
  double x, y;
  size_t group;
} observation_t, observation_2d_t;

typedef struct observation_3d {
  double x, y, z;
  size_t group;
} observation_3d_t;

typedef struct cluster_2d {
  double x, y;
  size_t count;
} cluster_t, cluster_2d_t;

typedef struct cluster_3d {
  double x, y, z;
  size_t count;
} cluster_3d_t;

cluster_t *k_means(observation_t observations[], size_t size, size_t k);

cluster_2d_t *k_means_2d(observation_2d_t observations[], size_t size, size_t k);

cluster_3d_t *k_means_3d(observation_3d_t observations[], size_t size, size_t k);
