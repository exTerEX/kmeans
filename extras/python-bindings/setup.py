#!/usr/bin/env python
import setuptools
import Cython

kmeans_extension = setuptools.Extension(
    "kmeans.kmeans_ext",
    language="c",
    sources=["src/kmeans/kmeans_ext.pyx"],
    libraries=["kmeans"]
)

with open("README.md", "r", encoding="utf-8") as file:
    long_description = file.read()

with open("requirements/requirements-setup.txt", "r", encoding="utf-8") as file:
    setup_requires = file.read()

with open("requirements/requirements.txt", "r", encoding="utf-8") as file:
    install_requires = file.read()

if __name__ == "__main__":
    setuptools.setup(
        name="KMeans",
        version="0.0.1",
        description="Wrapper to native \"kmeans\" library",
        long_description=long_description,
        long_description_content_type="text/markdown",
        author="Andreas Sagen",
        author_email="developer@sagen.io",
        url="https://github.com/exterex/kmeans/extras/python-bindings",
        packages=["kmeans"],
        ext_modules=Cython.Build.cythonize(
            kmeans_extension,
            language_level=3.6,
            compiler_directives={"linetrace": True}
        ),
        package_dir={"": "src"},
        package_data={
            "kmeans": ["kmeans_ext.pxd", "c_kmeans.pxd"]
        },
        include_package_data=True,
        setup_requires=setup_requires.splitlines(),
        zip_safe=False,
        install_requires=install_requires.splitlines(),
        keywords=[
            "Clustering",
            "K-Means"
        ],
        classifiers=[
            "Development Status :: 3 - Alpha",
            "License :: OSI Approved :: MIT License",
            "Natural Language :: English",
            "Operating System :: OS Independent",
            "Programming Language :: Cython",
            "Programming Language :: C",
            "Programming Language :: Python :: Implementation :: CPython",
            "Topic :: Software Development :: Libraries",
        ],
        license="MIT"
    )
