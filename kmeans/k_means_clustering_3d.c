#include "k_means_clustering.h"
#include <float.h>
#include <string.h>

#ifdef __STDC_LIB_EXT1__
#define E 1
#endif
#ifndef __STDC_LIB_EXT1__
#define E 2
#endif

#define MIN_ERROR_DENOMINATOR_SIZE 10000

size_t calculate_nearst(observation_3d_t *observation, cluster_3d_t clusters[], size_t k) {
  double min_distance = DBL_MAX;
  double distance = 0;

  size_t nearest_index = -1;

  for (size_t index = 0; index < k; index++) {
    distance = (clusters[index].x - observation->x) * (clusters[index].x - observation->x) +
               (clusters[index].y - observation->y) * (clusters[index].y - observation->y) +
               (clusters[index].z - observation->z) * (clusters[index].z - observation->z);

    if (distance < min_distance) {
      min_distance = distance;
      nearest_index = index;
    }
  }
  return nearest_index;
}

void calculate_centroid(observation_3d_t observations[], size_t size, cluster_3d_t *centroid) {
  centroid->x = 0;
  centroid->y = 0;
  centroid->z = 0;
  centroid->count = size;

  for (size_t index = 0; index < size; index++) {
    centroid->x += observations[index].x;
    centroid->y += observations[index].y;
    centroid->z += observations[index].z;
    observations[index].group = 0;
  }

  centroid->x /= centroid->count;
  centroid->y /= centroid->count;
  centroid->z /= centroid->count;
}

cluster_3d_t *k_means_3d(observation_3d_t observations[], size_t size, size_t k) {
  cluster_3d_t *clusters = NULL;

  if (k <= 1) {
    clusters = (cluster_3d_t *)malloc(sizeof(cluster_3d_t));
    memset(clusters, 0, sizeof(cluster_3d_t));
    calculate_centroid(observations, size, clusters);
  } else if (k < size) {
    clusters = malloc(sizeof(cluster_3d_t) * k);
    memset(clusters, 0, k * sizeof(cluster_3d_t));

    for (size_t index = 0; index < size; index++) {
      observations[index].group = rand() % k;
    }

    size_t changed = 0;
    size_t min_error = size / MIN_ERROR_DENOMINATOR_SIZE;

    size_t temp = 0;

    do {
      for (size_t index = 0; index < k; index++) {
        clusters[index].x = 0;
        clusters[index].y = 0;
        clusters[index].z = 0;
        clusters[index].count = 0;
      }

      for (size_t index = 0; index < size; index++) {
        temp = observations[index].group;

        clusters[temp].x += observations[index].x;
        clusters[temp].y += observations[index].y;
        clusters[temp].z += observations[index].z;
        clusters[temp].count++;
      }

      for (size_t index = 0; index < k; index++) {
        clusters[index].x /= clusters[index].count;
        clusters[index].y /= clusters[index].count;
        clusters[index].z /= clusters[index].count;
      }

      changed = 0;
      for (size_t index = 0; index < size; index++) {
        temp = calculate_nearst(observations + index, clusters, k);

        if (temp != observations[index].group) {
          changed++;
          observations[index].group = temp;
        }
      }
    } while (changed > min_error);
  } else {
    clusters = (cluster_3d_t *)malloc(sizeof(cluster_3d_t) * k);
    memset(clusters, 0, k * sizeof(cluster_3d_t));

    for (size_t index = 0; index < size; index++) {
      clusters[index].x = observations[index].x;
      clusters[index].y = observations[index].y;
      clusters[index].z = observations[index].z;

      clusters[index].count = 1;
      observations[index].group = index;
    }
  }
  return clusters;
}
