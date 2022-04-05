License solver
============================

Welcome to Thoth's license-solver repository!

This tool handles license and classifier detection from metadata provided by PyPI. Determines the type of license and its version. It also indicates a discrepancy in the license and in the classifier.


What license-solver does
------------------------
Detects licenses and classifier from metadata provided by:

* PyPI
* JSON files
* folders with JSON files
* dictionary (with function *detect_license()*)

The output is printed by default on STDOUT (you can choose the file where to save the output more in --help).


Good to know
^^^^^^^^^^^^

* unidentified license/version/classifier are named `UNDETECTED`
* non-versioned licenses have an identifier in license_version `LICENSE-WITHOUT-VERSION`


Run solver locally
^^^^^^^^^^^^^^^^^^
Often, it is useful to run license-solver locally to experiment or verify your changes in implementation. You can do so easily
by running:


.. code-block:: console

   $ PYTHONPATH=. python3 ./thoth-license-solver <arguments>


Examples
^^^^^^^^

1. sample with 1 `file <https://github.com/thoth-station/license-solver/tree/master/tests/examples/request_example.json>`_:

.. code-block:: console

    $ thoth-license-solver --file tests/examples/request_example.json -pp 4

* Output 1.:

.. code:: json

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

------------



2. sample with 2 `files <https://github.com/thoth-station/license-solver/tree/master/tests/examples/>`_ with the same package but with different versions:

.. code-block:: console

   $ thoth-license-solver --file tests/examples/request_example.json tests/examples/request_example_2.json -pp 4


* Output 2.

.. code-block:: json

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

------------


3. sample with 2  `files <https://github.com/thoth-station/license-solver/tree/master/tests/examples/>`_ with the same package but with different versions and with 1 different PyPI package:

.. code-block:: console

   $ thoth-license-solver --file tests/examples/request_example.json tests/examples/request_example_2.json --package-name numpy -pp 4

* Output 3.

.. code-block:: json

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


Installation
^^^^^^^^^^^^

Install `license-solver`:

.. code-block:: console

   $ pip install thoth-license-solver


Run tests
^^^^^^^^^
It is a good habit for the program to be tested after the implementation of new features. You can run:

.. code-block:: console

   $ pytest tests/
   # or
   $ pytest --cov-report term-missing --cov=thoth tests/     # coverage test


Special aliases
^^^^^^^^^^^^^^^
- default BSD naming is 4th clause ([source](https://en.wikipedia.org/wiki/BSD_licenses#Terms))
