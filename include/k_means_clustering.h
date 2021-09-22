#include <stdlib.h>

typedef struct observation {
    double x, y;
    size_t group;
} observation_t;

typedef struct cluster {
    double x, y;
    size_t count;
} cluster_t;

cluster_t *k_means(observation_t observations[], size_t size, size_t k);