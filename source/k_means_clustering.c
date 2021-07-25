/*
 * Copyright 2021 Andreas Sagen
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at

 *     http://www.apache.org/licenses/LICENSE-2.0

 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

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

size_t calculate_nearst(observation_t *observation, cluster_t clusters[], size_t k) {
    double min_distance = DBL_MAX;
    double distance = 0;

    size_t nearest_index = -1;

    for (size_t index = 0; index < k; index++) {
        distance = (clusters[index].x - observation->x) * (clusters[index].x - observation->x) +
                   (clusters[index].y - observation->y) * (clusters[index].y - observation->y);

        if (distance < min_distance) {
            min_distance = distance;
            nearest_index = index;
        }
    }
    return nearest_index;
}

void calculate_centroid(observation_t observations[], size_t size, cluster_t *centroid) {
    centroid->x = 0;
    centroid->y = 0;
    centroid->count = size;

    for (size_t index = 0; index < size; index++) {
        centroid->x += observations[index].x;
        centroid->y += observations[index].y;
        observations[index].group = 0;
    }

    centroid->x /= centroid->count;
    centroid->y /= centroid->count;
}

cluster_t *k_means(observation_t observations[], size_t size, size_t k) {
    cluster_t *clusters = NULL;

    if (k <= 1) {
        clusters = (cluster_t *)malloc(sizeof(cluster_t));
        memset(clusters, 0, sizeof(cluster_t));
        calculate_centroid(observations, size, clusters);
    } else if (k < size) {
        clusters = malloc(sizeof(cluster_t) * k);
        memset(clusters, 0, k * sizeof(cluster_t));

        for (size_t index = 0; index < size; index++) {
            observations[index].group = rand() % k; // NOLINT(cert-msc30-c, cert-msc50-cpp)
        }

        size_t changed = 0;
        size_t min_error = size / MIN_ERROR_DENOMINATOR_SIZE;

        size_t temp = 0;

        do {
            for (size_t index = 0; index < k; index++) {
                clusters[index].x = 0;
                clusters[index].y = 0;
                clusters[index].count = 0;
            }

            for (size_t index = 0; index < size; index++) {
                temp = observations[index].group;
                clusters[temp].x += observations[index].x;
                clusters[temp].y += observations[index].y;
                clusters[temp].count++;
            }

            for (size_t index = 0; index < k; index++) {
                clusters[index].x /= clusters[index].count;
                clusters[index].y /= clusters[index].count;
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
        clusters = (cluster_t *)malloc(sizeof(cluster_t) * k);
        memset(clusters, 0, k * sizeof(cluster_t));
        for (size_t index = 0; index < size; index++) {
            clusters[index].x = observations[index].x;
            clusters[index].y = observations[index].y;
            clusters[index].count = 1;
            observations[index].group = index;
        }
    }
    return clusters;
}