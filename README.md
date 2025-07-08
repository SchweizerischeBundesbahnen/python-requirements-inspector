[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=SchweizerischeBundesbahnen_python-requirements-inspector&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=SchweizerischeBundesbahnen_python-requirements-inspector)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=SchweizerischeBundesbahnen_python-requirements-inspector&metric=bugs)](https://sonarcloud.io/summary/new_code?id=SchweizerischeBundesbahnen_python-requirements-inspector)
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=SchweizerischeBundesbahnen_python-requirements-inspector&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=SchweizerischeBundesbahnen_python-requirements-inspector)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=SchweizerischeBundesbahnen_python-requirements-inspector&metric=coverage)](https://sonarcloud.io/summary/new_code?id=SchweizerischeBundesbahnen_python-requirements-inspector)
[![Duplicated Lines (%)](https://sonarcloud.io/api/project_badges/measure?project=SchweizerischeBundesbahnen_python-requirements-inspector&metric=duplicated_lines_density)](https://sonarcloud.io/summary/new_code?id=SchweizerischeBundesbahnen_python-requirements-inspector)
[![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=SchweizerischeBundesbahnen_python-requirements-inspector&metric=ncloc)](https://sonarcloud.io/summary/new_code?id=SchweizerischeBundesbahnen_python-requirements-inspector)
[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=SchweizerischeBundesbahnen_python-requirements-inspector&metric=reliability_rating)](https://sonarcloud.io/summary/new_code?id=SchweizerischeBundesbahnen_python-requirements-inspector)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=SchweizerischeBundesbahnen_python-requirements-inspector&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=SchweizerischeBundesbahnen_python-requirements-inspector)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=SchweizerischeBundesbahnen_python-requirements-inspector&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=SchweizerischeBundesbahnen_python-requirements-inspector)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=SchweizerischeBundesbahnen_python-requirements-inspector&metric=vulnerabilities)](https://sonarcloud.io/summary/new_code?id=SchweizerischeBundesbahnen_python-requirements-inspector)

# Python module to inspect any type of functional or non-functional requirements

This module uses [spaCy](https://github.com/explosion/spaCy) to inspect requirements written in English or German.
For each requirement a report will be generated with information about the complexity, usage of weak words, usage of non-passive sentences, etc


# Prerequisites
This project requires Python 3.12 and Poetry for dependency management.

## Setup Environment
```bash
# Ensure Poetry uses Python 3.12
poetry env use python3.12

# Install dependencies (including test dependencies)
poetry install --all-extras
```

# How to test and build
This module can be produced using poetry:
```bash
poetry run pre-commit run -a
poetry run tox
poetry build
```

# How to install
## Poetry project
```bash
poetry add https://github.com/SchweizerischeBundesbahnen/python-requirements-inspector/releases/download/4.0.0/python_requirements_inspector-4.0.0-py3-none-any.whl
```

# How to use (example)
## Inputs are defined in inputs.json
```json
[
  {
    "id": "requirements1",
    "title": "I'm a title without a processword",
    "description":"I'm a description for testing with a weakword accordingly",
    "language":"en"
  },
  {
    "id": "requirements2",
    "title": "Ich bin ein Titel ohne Processwort",
    "description":"öüäß Ich bin eine Beschreibung mit dem Weakword entsprechend und Umlauts.",
    "language":"de"
  }
]
```
## Execute
```bash
poetry run inspect-requirements path/to/input/json
```
## Outputs will be returned in /tmp/output_*.json
```json
[
  {"id": "requirements1",
    "language": "en",
    "smellDescription": "In TITLE missingProcessword: Title contains no process word\nIn DESCRIPTION Sentence 1 I'm a\u2026 smellWeakword: accordingly [9] \n",
    "smellComplex": 0,
    "smellPassive": 0,
    "smellWeakword": 1,
    "smellComparative": 0,
    "missingProcessword": true
  },
  {
    "id": "requirements2",
    "language": "de",
    "smellDescription": "In TITLE missingProcessword: Title contains no process word\nIn DESCRIPTION Sentence 1 \u00f6\u00fc\u00e4\u00df Ich bin\u2026 smellWeakword: entsprechend [8] \n",
    "smellComplex": 0,
    "smellPassive": 0,
    "smellWeakword": 1,
    "smellComparative": 0,
    "missingProcessword": true
  }
]
```
