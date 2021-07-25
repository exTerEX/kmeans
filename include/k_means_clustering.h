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