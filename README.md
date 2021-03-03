[![PyPI](https://img.shields.io/pypi/v/beam-bc365.svg)](https://pypi.org/project/beam-bc365/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/beam-bc365.svg)](https://pypi.org/project/beam-bc365/)
[![CI/CD](https://github.com/Spazzy757/beam-bc365/actions/workflows/cicd.yaml/badge.svg)](https://github.com/Spazzy757/beam-bc365/actions/workflows/cicd.yaml)

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

# Usage

The intended use of this libary is to Pull Data from Microsoft Central Business Central [Web Services](https://docs.microsoft.com/en-us/dynamics365/business-central/dev-itpro/webservices/web-services#odata-web-services)

```python
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from beam_bc365.io import bc_service

service_config = bc_service.ServiceConfiguration(
    username='foo',
    service_key='api-key',
    companies=['Cranos'],
    service='G_L_ENTRY',
    instance='Sandbox',
    instance_id="2E0B815D-A1AC-491B-BD09-0876DACC2A12"
)
with beam.Pipeline(options=PipelineOptions()) as p:
    records = p | "Reading records from service" >>  bc_service.ReadFromService(
        service_config=service_config,
    )
    records | 'Writing to stdout' >> beam.Map(print)
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
