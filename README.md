# License solver
Welcome to Thoth's license-solver repository!

This tool handles license and classifier detection from metadata provided by PyPI. Determines the type of license and its version. It also indicates a discrepancy in the license and in the classifier.

## What license-solver does
Detects licenses and classifier from metadata provided by:
   - PyPI
   - JSON files
   - folder/s with JSON files
   - dictionary

The output is printed by default on STDOUT (you can choose the file where to save the output more in --help).

## Good to know
- unidentified license/version/classifier are named `UNDETECTED`
- non-versioned licenses have an identifier in license_version `LICENSE-WITHOUT-VERSION`

## Special aliases
- default BSD naming is 4th clause ([source](https://en.wikipedia.org/wiki/BSD_licenses#Terms))

## Important aliases
This section provides information about specific implementation detail, which can be not obviously clear.
- `BSD` license name in metadata without specific clause is `4-clause BSD` in license-solver implementation ([source](https://en.wikipedia.org/wiki/BSD_licenses#Terms))

## Run solver locally
Often, it is useful to run license-solver locally to experiment or verify your changes in implementation. You can do so easily
by running:
```shell
$ PYTHONPATH=. python3 ./thoth-license-solver <arguments>
```

## Examples
1. sample with 1 [file](https://github.com/thoth-station/license-solver/tree/master/tests/examples/request_example.json)
    ```shell
    $ thoth-license-solver --file tests/examples/request_example.json -pp 4
    ```
    Output:
    ```json
    {
        "requests": {
            "2.27.1": {
                "license": [
                    "Apache License 2.0",
                    "Apache-2.0",
                    "Apache 2.0"
                ],
                "license_version": "2.0",
                "classifier": [
                    [
                        "License :: OSI Approved :: Apache Software License",
                        "Apache Software License"
                    ]
                ],
                "warning": false
            }
        }
    }
    ```
2. sample with 2 [files](https://github.com/thoth-station/license-solver/tree/master/tests/examples/) with the same package but with different versions
    ```shell
    $ thoth-license-solver --file tests/examples/request_example.json tests/examples/request_example_2.json -pp 4
    ```
    Output:
    ```json
    {
        "requests": {
            "2.27.1": {
                "license": [
                    "Apache License 2.0",
                    "Apache-2.0",
                    "Apache 2.0"
                ],
                "license_version": "2.0",
                "classifier": [
                    [
                        "License :: OSI Approved :: Apache Software License",
                        "Apache Software License"
                    ]
                ],
                "warning": false
            },
            "2.24.0": {
                "license": [
                    "Apache License 2.0",
                    "Apache-2.0",
                    "Apache 2.0"
                ],
                "license_version": "2.0",
                "classifier": [
                    [
                        "License :: OSI Approved :: Apache Software License",
                        "Apache Software License"
                    ]
                ],
                "warning": false
            }
        }
    }
    ```
3. sample with 2  [files](https://github.com/thoth-station/license-solver/tree/master/tests/examples/) with the same package but with different versions and with 1 different PyPI package
    ```shell
    $ thoth-license-solver --file tests/examples/request_example.json tests/examples/request_example_2.json --package-name numpy -pp 4
    ```
    output:
    ```json
    {
        "numpy": {
            "1.22.1": {
                "license": [
                    "BSD 4-Clause \"Original\" or \"Old\" License",
                    "BSD-4-Clause",
                    "BSD 4 Clause"
                ],
                "license_version": "4",
                "classifier": [
                    [
                        "License :: OSI Approved :: BSD License",
                        "BSD License"
                    ]
                ],
                "warning": false
            }
        },
        "requests": {
            "2.27.1": {
                "license": [
                    "Apache License 2.0",
                    "Apache-2.0",
                    "Apache 2.0"
                ],
                "license_version": "2.0",
                "classifier": [
                    [
                        "License :: OSI Approved :: Apache Software License",
                        "Apache Software License"
                    ]
                ],
                "warning": false
            },
            "2.24.0": {
                "license": [
                    "Apache License 2.0",
                    "Apache-2.0",
                    "Apache 2.0"
                ],
                "license_version": "2.0",
                "classifier": [
                    [
                        "License :: OSI Approved :: Apache Software License",
                        "Apache Software License"
                    ]
                ],
                "warning": false
            }
        }
    }

    ```

## Installation
Install `license-solver`:
```shell
$ pip install thoth-license-solver
```

## Run tests
It is a good habit for the program to be tested after the implementation of new features. You can run:
```shell
$ pytest tests/
# or
$ pytest --cov-report term-missing --cov=thoth tests/     # coverage test
```
