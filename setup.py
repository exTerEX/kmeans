#!/usr/bin/env python

from __future__ import print_function

import distutils.command.install_data
import os
import pathlib
import platform
import shutil
import sys
import setuptools
import setuptools.command.build_ext
import setuptools.command.install_lib
import setuptools.command.install_scripts

if sys.version_info < (3,):
    print("Python 2 has reached end-of-life and is no longer supported by PyTorch.")
    sys.exit(-1)

python_min_version = (3, 7, 0)
python_min_version_str = '.'.join(map(str, python_min_version))

if sys.version_info < python_min_version:
    print("You are using Python {}. Python >={} is required.".format(platform.python_version(),
                                                                     python_min_version_str))
    sys.exit(-1)

PACKAGE_NAME = "kmeans"


class CMakeExtension(setuptools.Extension):
    """
    An extension to run the cmake build

    This simply overrides the base extension class so that setuptools
    doesn't try to build your sources for you.
    """

    def __init__(self, name, sources=[]):
        super().__init__(name=name, sources=sources)


class install_data(distutils.command.install_data.install_data):
    """
    Just a wrapper to get the install data into the egg-info

    Listing the installed files in the egg-info guarantees that
    all of the package files will be uninstalled when the user
    uninstalls your package through pip
    """

    def run(self):
        """
        Outfiles are the libraries that were built using cmake
        """
        self.outfiles = self.distribution.data_files


class install_lib(setuptools.command.install_lib.install_lib):
    """
    Get the libraries from the parent distribution, use those as the outfiles

    Skip building anything; everything is already built, forward libraries to
    the installation step
    """

    def run(self):
        """
        Copy libraries from the bin directory and place them as appropriate
        """

        self.announce("Moving library files", level=3)

        self.skip_build = True

        bin_dir = self.distribution.bin_dir

        libs = [
            os.path.join(bin_dir, _lib) for _lib in
            os.listdir(bin_dir) if
            os.path.isfile(os.path.join(bin_dir, _lib)) and
            os.path.splitext(_lib)[1] in [".dll", ".so"]
            and not (_lib.startswith("python") or _lib.startswith(PACKAGE_NAME))
        ]

        for lib in libs:
            shutil.move(lib, os.path.join(self.build_dir, os.path.basename(lib)))

        # These are the additional installation files that should be
        # included in the package, but are resultant of the cmake build
        # step; depending on the files that are generated from your cmake
        # build chain, you may need to modify the below code

        self.distribution.data_files = [
            os.path.join(
                self.install_dir,
                os.path.basename(lib)) for lib in libs
        ]

        self.distribution.run_command("install_data")

        super().run()


class install_scripts(setuptools.command.install_scripts.install_scripts):
    """
    Install the scripts in the build dir
    """

    def run(self):
        """
        Copy the required directory to the build directory and super().run()
        """

        self.announce("Moving scripts files", level=3)

        self.skip_build = True

        bin_dir = self.distribution.bin_dir

        scripts_dirs = [
            os.path.join(bin_dir, _dir) for _dir in
            os.listdir(bin_dir) if
            os.path.isdir(os.path.join(bin_dir, _dir))
        ]

        for scripts_dir in scripts_dirs:
            shutil.move(scripts_dir,
                        os.path.join(self.build_dir,
                                     os.path.basename(scripts_dir)))

        # Mark the scripts for installation, adding them to
        # distribution.scripts seems to ensure that the setuptools' record
        # writer appends them to installed-files.txt in the package's egg-info

        self.distribution.scripts = scripts_dirs

        super().run()


"""
class build_ext(setuptools.command.build_ext.build_ext):

    def run(self):
        for ext in self.extensions:
            self.build_cmake(ext)
        super().run()

    def build_cmake(self, ext):

        cwd = pathlib.Path().absolute()

        build_dir = pathlib.Path(self.build_temp)
        build_dir.mkdir(parents=True, exist_ok=True)
        extension_path = pathlib.Path(self.get_ext_fullpath(ext.name))
        extension_path.mkdir(parents=True, exist_ok=True)

        config = "Debug" if self.debug else "Release"
        cmake_args = [
            "-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=" + str(extension_path.parent.absolute()),
            "-DCMAKE_BUILD_TYPE=" + config
        ]

        build_args = ["--config", config, "--", "-j4"]

        os.chdir(str(build_dir))
        self.spawn(["cmake", str(cwd)] + cmake_args)
        if not self.dry_run:
            self.spawn(["cmake", "--build", "."] + build_args)
        os.chdir(str(cwd))
"""


class build_ext(setuptools.command.build_ext.build_ext):
    """
    Builds using cmake instead of the python setuptools implicit build
    """

    def run(self):
        """
        Perform build_cmake before doing the 'normal' stuff
        """

        for extension in self.extensions:
            self.build_cmake(extension)

        super().run()

    def build_cmake(self, extension: setuptools.Extension):
        """
        The steps required to build the extension
        """

        self.announce("Preparing the build environment", level=3)

        cwd = pathlib.Path().absolute()

        build_dir = pathlib.Path(self.build_temp)
        os.makedirs(build_dir, exist_ok=True)

        extension_path = pathlib.Path(self.get_ext_fullpath(extension.name))
        os.makedirs(extension_path.parent.absolute(), exist_ok=True)

        self.announce("Configuring cmake project", level=3)

        config = "Debug" if self.debug else "Release"

        config_args = [
            "-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=" + str(extension_path.parent.absolute()),
            "-DCMAKE_BUILD_TYPE=" + config
        ]
        build_args = ["--config", config, "--", "-j4"]

        self.spawn(["cmake", str(cwd), "-B" + self.build_temp] + config_args)

        if not self.dry_run:
            self.announce("Building binaries", level=3)

            self.spawn(["cmake", "--build", self.build_temp] + build_args)

            self.announce("Moving built python module", level=3)

            # Add more subolders if changes to CMAKE_*_OUTPUT_DIRECTORY in CMakeLists.txt
            self.distribution.bin_dir = bin_dir = os.path.join(build_dir)

            pyd_path = [
                os.path.join(bin_dir, _pyd) for _pyd in
                os.listdir(bin_dir) if
                os.path.isfile(os.path.join(bin_dir, _pyd)) and
                os.path.splitext(_pyd)[0].startswith(PACKAGE_NAME) and
                os.path.splitext(_pyd)[1] in [".pyd", ".so"]
            ][0]

            shutil.move(pyd_path, extension_path)


with open("README.md", "r", encoding="utf-8") as file:
    long_description = file.read()


if __name__ == "__main__":
    setuptools.setup(
        name="kmeans",
        license="MIT",
        author="Andreas Sagen",
        description="A kmeans clustering algorithm implemented in C",
        long_description=long_description,
        long_description_content_type="text/markdown",
        packages=setuptools.find_packages(where="python"),
        install_requires=[
            "numpy"
        ],
        package_data={
            "kmeans": [
                "lib/*.so",
                "include/kmeans/*.h"
            ]
        },
        setup_requires=[
            "setuptools>=51.0.0",
            "wheel>=0.29.0",
            "setuptools-git-versioning"
        ],
        ext_modules=[CMakeExtension("kmeans")],
        cmdclass={
            "build_ext": build_ext,
            "install_data": install_data,
            "install_lib": install_lib,
            "install_scripts": install_scripts
        },
        python_requires=">=3.7",
        platforms=["any"]
    )
