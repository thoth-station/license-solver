# License solver

Welcome to Thoth's license-solver repository

This repository serves for license detection and classifier detection from PyPI metadata.

## How it works

license-solver detect licenses and classifiers from input files/directory. If the solver can't find a license or
classifier related to the supported name, then the result is for them `UNKNOWN`, for undetected license version
is `UNDETECTED`. Some licenses do not have versions, and their naming is `LICENSE-WITHOUT-VERSION`. All dictionaries with the most used aliases are stored in thoth/license_solver/data. <br>
After successful detection, license and classifier will be compared. If they don't match, then in final JSON will be
warning: True. In case if it is missing license or classifier, comparing will be aborted. <br>
In final will be printed JSON on STDOUT.

## Important aliases
license name:
- `BSD` without clause = 4 clause BSD ([source](https://en.wikipedia.org/wiki/BSD_licenses#Terms))

classifier:
- None for now

## Run solver locally

Often, it is useful to run adviser locally to experiment or verify your changes in implementation. You can do so easily
by running:

```
PYTHONPATH=. python3 ./thoth-license-solver <arguments>
```

## Run tests

It is a good habit for the program to be tested after the implementation of new features. You can run:

```
pytest tests/
pytest --cov-report term-missing --cov=thoth tests/ # get test coverage
```
