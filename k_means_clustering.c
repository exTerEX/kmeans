/**
 * @file k_means_clustering.c
 * @author Andreas Sagen (developer@sagen.io)
 * @brief K-Means Clustering algorithm
 * @version 1.0.0
 * @date 2021-02-13
 *
 * @copyright Copyright 2021 Andreas Sagen
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

int calculate_nearst(observation *observation, cluster clusters[], int k) {
    double min_distance = DBL_MAX;
    double distance = 0;

    int nearest_index = -1;

    for (int index = 0; index < k; index++) {
        distance = (clusters[index].x - observation->x) * (clusters[index].x - observation->x) +
                   (clusters[index].y - observation->y) * (clusters[index].y - observation->y);

        if (distance < min_distance) {
            min_distance = distance;
            nearest_index = index;
        }
    }
    return nearest_index;
}

void calculate_centroid(observation observations[], size_t size, cluster *centroid) {
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

cluster *k_means(observation observations[], size_t size, int k) {
    cluster *clusters = NULL;

    if (k <= 1) {
        clusters = (cluster *)malloc(sizeof(cluster));
        memset(clusters, 0, sizeof(cluster));
        calculate_centroid(observations, size, clusters);
    } else if (k < size) {
        clusters = malloc(sizeof(cluster) * k);
        memset(clusters, 0, k * sizeof(cluster));

        for (size_t index = 0; index < size; index++) {
            observations[index].group = rand() % k;
        }

        size_t changed = 0;
        size_t min_error = size / 10000;

        int temp = 0;

        do {
            for (int index = 0; index < k; index++) {
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

            for (int index = 0; index < k; index++) {
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
        clusters = (cluster *)malloc(sizeof(cluster) * k);
        memset(clusters, 0, k * sizeof(cluster));
        for (int index = 0; index < size; index++) {
            clusters[index].x = observations[index].x;
            clusters[index].y = observations[index].y;
            clusters[index].count = 1;
            observations[index].group = index;
        }
    }
    return clusters;
}