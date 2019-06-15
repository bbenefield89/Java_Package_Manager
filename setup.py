import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Java Package Manager",
    version="0.0.5",
    author="Author Name",
    author_email="bsquared18@gmail.com",
    description="A small CLI package manager for Java projects using Maven",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    scripts=[
        'bin/jpm'
    ],
)