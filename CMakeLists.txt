cmake_minimum_required(VERSION 3.1 FATAL_ERROR)

project(kmeans LANGUAGES C)

set(CMAKE_C_STANDARD 99)

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR})
set(CMAKE_EXECUTABLE_SUFFIX .exe)

find_library(MATH REQUIRED)

add_executable(${PROJECT_NAME} main.c k_means_clustering.c)

if(MATH_LIBRARY)
  target_link_libraries(${PROJECT_NAME} ${MATH_LIBRARY})
endif()
