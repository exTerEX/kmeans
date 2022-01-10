cmake_minimum_required(VERSION 3.1 FATAL_ERROR)

project(kmeans LANGUAGES C)

include_directories(include)

set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED True)

find_library(MATH_LIBRARY m REQUIRED)

if ("${CMAKE_BUILD_TYPE}" STREQUAL "Debug")
  set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR})
endif ()

# library
add_library(${PROJECT_NAME} SHARED src/2d.c src/3d.c)
target_include_directories(
  ${PROJECT_NAME} PUBLIC $<BUILD_INTERFACE:${CMAKE_SOURCE_DIR}/include>
                         $<INSTALL_INTERFACE:include>)
set_target_properties(
  ${PROJECT_NAME}
  PROPERTIES LINKER_LANGUAGE C
             C_STANDARD 11)

# executable
if ("${CMAKE_BUILD_TYPE}" STREQUAL "Debug")
  add_executable(main examples/main.c)
  set_target_properties(main PROPERTIES LINKER_LANGUAGE C C_STANDARD 11)

  if (MATH_LIBRARY)
    target_link_libraries(main ${PROJECT_NAME} ${MATH_LIBRARY})
  endif ()
endif ()
