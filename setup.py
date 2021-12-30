#!/usr/bin/env python
import os
import pathlib

from setuptools import Extension, find_packages, setup
from setuptools.command.build_ext import build_ext


class CMakeExtension(Extension):
    def __init__(self, name):
        super().__init__(name, sources=[])


class build_ext(build_ext):
    def run(self):
        for ext in self.extensions:
            self.build_cmake(ext)
        super().run()

    def build_cmake(self, ext):
        cwd = pathlib.Path().absolute()

        build_temp = pathlib.Path(self.build_temp)
        build_temp.mkdir(parents=True, exist_ok=True)
        extdir = pathlib.Path(self.get_ext_fullpath(ext.name))
        extdir.mkdir(parents=True, exist_ok=True)

        config = "Debug" if self.debug else "Release"
        cmake_args = [
            "-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=" + str(extdir.parent.absolute()),
            "-DCMAKE_BUILD_TYPE=" + config]

        build_args = ["--config", config, "--", "-j4"]

        os.chdir(str(build_temp))
        self.spawn(["cmake", str(cwd)] + cmake_args)
        if not self.dry_run:
            self.spawn(["cmake", "--build", "."] + build_args)
        os.chdir(str(cwd))


with open("README.md", "r", encoding="utf-8") as file:
    long_description = file.read()


if __name__ == "__main__":
    setup(
        name="kmeans",
        version="0.1.0",
        license="LGPL-3.0-or-later",
        author="Andreas Sagen",
        description="A kmeans clustering algorithm implemented in C",
        long_description=long_description,
        long_description_content_type="text/markdown",
        packages=find_packages(where="lib/python/kmeans"),
        package_data={
            "kmeans": ["libkmeans.so"]
        },
        ext_modules=[CMakeExtension("kmeans")],
        cmdclass={"build_ext": build_ext},
        python_requires=">=3.6",
        install_requires=["numpy"]
    )
