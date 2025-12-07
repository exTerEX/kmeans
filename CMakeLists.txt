cmake_minimum_required(VERSION 3.15)

project(kmeans VERSION 0.1.0 LANGUAGES C)

set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)

find_package(Python REQUIRED COMPONENTS Interpreter Development.Module NumPy)

include_directories(include)

find_library(MATH_LIBRARY m)

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${PROJECT_BINARY_DIR})
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${PROJECT_BINARY_DIR})
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${PROJECT_BINARY_DIR})

# Shared library for C API (optional, for non-Python usage)
if(EXISTS "${CMAKE_SOURCE_DIR}/src/2d.c" AND EXISTS "${CMAKE_SOURCE_DIR}/src/3d.c")
  add_library(${PROJECT_NAME}_lib SHARED src/2d.c src/3d.c)
  target_include_directories(${PROJECT_NAME}_lib PUBLIC 
    $<BUILD_INTERFACE:${CMAKE_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:include>
  )
  set_target_properties(${PROJECT_NAME}_lib PROPERTIES 
    LINKER_LANGUAGE C
    C_STANDARD 11
    OUTPUT_NAME "kmeans"
  )
  if(MATH_LIBRARY)
    target_link_libraries(${PROJECT_NAME}_lib ${MATH_LIBRARY})
  endif()
endif()

# Debug executable
if(CMAKE_BUILD_TYPE STREQUAL "Debug" AND EXISTS "${CMAKE_SOURCE_DIR}/examples/main.c")
  add_executable(main examples/main.c)
  set_target_properties(main PROPERTIES LINKER_LANGUAGE C C_STANDARD 11)
  if(TARGET ${PROJECT_NAME}_lib)
    target_link_libraries(main ${PROJECT_NAME}_lib)
  endif()
  if(MATH_LIBRARY)
    target_link_libraries(main ${MATH_LIBRARY})
  endif()
endif()

# Python extension module
python_add_library(_kmeans MODULE
    src/kmeans/_kmeans.c
    WITH_SOABI
)

target_include_directories(_kmeans PRIVATE
    ${Python_NumPy_INCLUDE_DIRS}
    ${CMAKE_SOURCE_DIR}/include
)

target_link_libraries(_kmeans PRIVATE Python::NumPy)

if(MATH_LIBRARY)
  target_link_libraries(_kmeans PRIVATE ${MATH_LIBRARY})
endif()

# Install the extension module
install(TARGETS _kmeans DESTINATION kmeans)
