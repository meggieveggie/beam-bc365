[![PyPI](https://img.shields.io/pypi/v/beam-bc365.svg)](https://pypi.org/project/beam-bc365/) [![PyPI - Downloads](https://img.shields.io/pypi/dm/beam-bc365.svg)](https://pypi.org/project/beam-bc365/)

# About

A collection of transforms for Microsoft Business Central 265 for the [Apache beam](https://beam.apache.org/) python SDK.

# Installation

- Using pip

```bash
pip install beam-bc3675
```

- From source

```bash
git clone git@github.com:Spazzy757/beam-bc365.git
cd beam-bc365
pip install .
```

# Local Development

## Install development dependencies

```bash
pip install -e .[dev]
```

## Run tests

```bash
nosetests
```

## Linting

please make sure to lint your code before contributing

```bash
pylint .
```

## Bumpversion

**NOTE:** This should be done by CI/CD, this is only for exceptional cases

This library uses semantic versioning

```bash
bump2version --new-version $NEW_VERSION setup.py
```
