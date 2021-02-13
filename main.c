#include "k_means_clustering.h"

#include <math.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

void main() {
    size_t size = 255L;
    observation *observations = (observation *)malloc(sizeof(observation) * size);

    for (int index = 0; index < size; index++) {
        double radius = 10 * ((double)rand() / RAND_MAX);
        double angle = 2 * M_PI * ((double)rand() / RAND_MAX);
        observations[index].x = radius * cos(angle);
        observations[index].y = radius * sin(angle);
    }

    int k = 10;
    cluster *clusters = k_means(observations, size, k);

    for (int index = 0; index < k; index++) {
        printf("Observations in cluster %i: %zu\n", index, clusters[index].count);
    }

    free(observations);
    free(clusters);
}