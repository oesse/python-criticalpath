# python-criticalpath
[![Build Status](https://travis-ci.org/oesse/python-criticalpath.svg?branch=master)](https://travis-ci.org/oesse/python-criticalpath)

This is a tool to find the critical path in the build process of Yocto
artifacts. It uses the information provided by the task dependency graph and a
build's "buildstats".

### Prerequisites

In order to find the critical path in the build process accurately you need to
run one build with all the targets that you are interested in, e.g. use a clean
build to also consider fetching, or use a build without sstate to consider even
cached steps. In this build you need to enable "buildstats", for example adding
the following to your `local.conf`:
```sh
INHERIT += "buildstats"
```
After the build, make note of your buildstats directory, e.g.
`build/tmp/buildstats/<timestamp>`.

Then, to generate the dependency graph  use bitbake:
```sh
bitbake -g <your-image>
```
This should generate `build/task-depends.dot`.

### Usage

Given that you have the dependency graph and the buildstats directory you can
find the critical path of the build using:
```sh
python -m criticalpath <path/to/task-depends.dot> <path/to/buildstats-dir> ...
```

It is possible to specify multiple buildstats directories, so that you can
reasonably combine, for example, a fetchall and an actual build in the same
critical path analysis.

### Dependencies

In order to run the tool you only need python >= 3.5.

### Run the tests

A `Makefile` is provided that will run the unit tests as well as the `flake8`
linter which has to be installed:
```sh
make test
```
