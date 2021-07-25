#include "k_means_clustering.h"

#include <math.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define INITIAL_MEANS (int)10
#define SIZE (size_t)255
#define MAX_RADIUS 10

int main(int argc, char **argv) {
    observation_t *observations = (observation_t *)malloc(sizeof(observation_t) * SIZE);

    for (int index = 0; index < SIZE; index++) {
        double radius = MAX_RADIUS * ((double)rand() / RAND_MAX);
        double angle = 2 * M_PI * ((double)rand() / RAND_MAX);
        observations[index].x = radius * cos(angle);
        observations[index].y = radius * sin(angle);
    }

    cluster_t *clusters = k_means(observations, SIZE, INITIAL_MEANS);

    for (int index = 0; index < INITIAL_MEANS; index++) {
        printf("Observations in cluster %i: %zu\n", index, clusters[index].count);
    }

    free(observations);
    free(clusters);
}