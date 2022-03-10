#!/usr/bin/env python3
# license-solver
# Copyright(C) 2021 Red Hat, Inc.
#
# This program is free software: you can redistribute it and / or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Setup configuration for adviser module."""

import os
import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand  # noqa


class Test(TestCommand):
    """Introduce test command to run testsuite using pytest."""

    _IMPLICIT_PYTEST_ARGS = [
        "--verbose",
        "-vv",
        "tests/",
    ]

    user_options = [("pytest-args=", "a", "Arguments to pass into py.test")]

    def initialize_options(self):
        """Initialize cli options."""
        super().initialize_options()
        self.pytest_args = None

    def finalize_options(self):
        """Finalize cli options."""
        super().finalize_options()
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        """Run module tests."""
        import pytest

        passed_args = list(self._IMPLICIT_PYTEST_ARGS)

        if self.pytest_args:
            self.pytest_args = [arg for arg in self.pytest_args.split() if arg]
            passed_args.extend(self.pytest_args)

        sys.exit(pytest.main(passed_args))


try:
    from setuptools import find_namespace_packages
except ImportError:
    # A dirty workaround for older setuptools.
    def find_namespace_packages(path="thoth"):
        """Find namespace packages alternative."""
        packages = set()
        for dir_name, dir_names, file_names in os.walk(path):
            if os.path.basename(dir_name) != "__pycache__":
                packages.add(dir_name.replace("/", "."))

        return sorted(packages)


def get_install_requires():
    """Get requirements for adviser module."""
    with open("requirements.txt", "r") as requirements_file:
        res = requirements_file.readlines()
        return [req.split(" ", maxsplit=1)[0] for req in res if req]


def get_version():
    """Get current version of adviser module."""
    with open(os.path.join("thoth", "license_solver", "__init__.py")) as f:
        content = f.readlines()

    for line in content:
        if line.startswith("__version__ ="):
            # dirty, remove trailing and leading chars
            return line.split(" = ")[1][1:-2]
    raise ValueError("No version identifier found")


def read(fname):
    """Read."""
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


VERSION = get_version()
setup(
    name="thoth-license-solver",
    version=VERSION,
    description="Package and package stack license-solver for the Thoth project",
    author="Viliam Podhajecky",
    author_email="vpodhaje@redhat.com",
    license="GPLv3+",
    long_description=read("README.rst"),
    packages=find_namespace_packages(),
    url="https://github.com/thoth-station/license-solver",
    package_data={
        "thoth.license_solver": [
            "data/comparator_dictionary.yaml",
            "data/license_dictionary.json",
            "data/pypi_classifiers.txt",
            "data/spdx_licenses.json",
            "data/license_without_versions.yaml",
            "py.typed",
        ]
    },
    entry_points={"console_scripts": ["thoth-license-solver=thoth.license_solver.cli:cli"]},
    zip_safe=False,
    install_requires=get_install_requires(),
    cmdclass={"test": Test},
    long_description_content_type="text/x-rst",
    command_options={
        "build_sphinx": {
            "version": ("setup.py", VERSION),
            "release": ("setup.py", VERSION),
        }
    },
)
