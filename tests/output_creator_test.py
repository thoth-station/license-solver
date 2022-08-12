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

"""Tests related to class OutputCreator."""

from typing import List, Dict
from thoth.license_solver.output_creator import OutputCreator
from thoth.license_solver.package import Package


class TestOutputCreator:
    """Test OutputCreator."""

    output_creator: OutputCreator = OutputCreator(False)

    @staticmethod
    def create_package(
        name: str,
        version: str,
        license_name: Dict[str, str],
        license_version: str,
        license_bool: bool,
        classifier: List[str],
    ) -> Package:
        """Create package."""
        license_list: List[str, str] = []

        if license_name:
            license_list = [license_name["full_name"], license_name["identifier_spdx"], license_name["identifier"]]

        package = Package()
        package.set_package_name(name)
        package.set_version(version)
        package.set_license((license_list, license_bool))
        package.set_license_version(license_version)
        package.set_classifier(classifier)

        return package

    def test_add_package_solo(self) -> None:
        """Test add_package solo versions."""
        package_1 = self.create_package(
            "test_1",
            "1.0",
            {"full_name": "MIT License", "identifier_spdx": "MIT", "identifier": "MIT"},
            "LICENSE-WITHOUT-VERSION",
            False,
            ["License :: OSI Approved :: MIT License", "MIT License"],
        )
        self.output_creator.add_package(package_1)

        assert self.output_creator.file == {
            "test_1": {
                "1.0": {
                    "license": {"full_name": "MIT License", "identifier_spdx": "MIT", "identifier": "MIT"},
                    "license_version": "LICENSE-WITHOUT-VERSION",
                    "classifier": [["License :: OSI Approved :: MIT License", "MIT License"]],
                    "warning": False,
                }
            }
        }

    def test_add_package_version_solo(self) -> None:
        """Test add_package solo versions."""
        package = self.create_package(
            "test_1",
            "1.1",
            {"full_name": "MIT License", "identifier_spdx": "MIT", "identifier": "MIT"},
            "LICENSE-WITHOUT-VERSION",
            False,
            ["License :: OSI Approved :: MIT License", "MIT License"],
        )
        self.output_creator.add_package(package)

        assert self.output_creator.file == {
            "test_1": {
                "1.0": {
                    "license": {"full_name": "MIT License", "identifier_spdx": "MIT", "identifier": "MIT"},
                    "license_version": "LICENSE-WITHOUT-VERSION",
                    "classifier": [["License :: OSI Approved :: MIT License", "MIT License"]],
                    "warning": False,
                },
                "1.1": {
                    "license": {"full_name": "MIT License", "identifier_spdx": "MIT", "identifier": "MIT"},
                    "license_version": "LICENSE-WITHOUT-VERSION",
                    "classifier": [["License :: OSI Approved :: MIT License", "MIT License"]],
                    "warning": False,
                },
            }
        }

    def test_add_package(self) -> None:
        """Test add_package."""
        package = self.create_package(
            "test_2",
            "1.0",
            {"full_name": "MIT License", "identifier_spdx": "MIT", "identifier": "MIT"},
            "LICENSE-WITHOUT-VERSION",
            False,
            ["License :: OSI Approved :: MIT License", "MIT License"],
        )
        self.output_creator.add_package(package)

        assert self.output_creator.file == {
            "test_1": {
                "1.0": {
                    "license": {"full_name": "MIT License", "identifier_spdx": "MIT", "identifier": "MIT"},
                    "license_version": "LICENSE-WITHOUT-VERSION",
                    "classifier": [["License :: OSI Approved :: MIT License", "MIT License"]],
                    "warning": False,
                },
                "1.1": {
                    "license": {"full_name": "MIT License", "identifier_spdx": "MIT", "identifier": "MIT"},
                    "license_version": "LICENSE-WITHOUT-VERSION",
                    "classifier": [["License :: OSI Approved :: MIT License", "MIT License"]],
                    "warning": False,
                },
            },
            "test_2": {
                "1.0": {
                    "license": {"full_name": "MIT License", "identifier_spdx": "MIT", "identifier": "MIT"},
                    "license_version": "LICENSE-WITHOUT-VERSION",
                    "classifier": [["License :: OSI Approved :: MIT License", "MIT License"]],
                    "warning": False,
                }
            },
        }

    def test_add_package_version(self) -> None:
        """Test add_package with version."""
        package = self.create_package(
            "test_2",
            "1.1",
            {"full_name": "MIT License", "identifier_spdx": "MIT", "identifier": "MIT"},
            "LICENSE-WITHOUT-VERSION",
            False,
            ["License :: OSI Approved :: Apache Software License", "Apache Software License"],
        )
        self.output_creator.add_package(package)

        assert self.output_creator.file == {
            "test_1": {
                "1.0": {
                    "license": {"full_name": "MIT License", "identifier_spdx": "MIT", "identifier": "MIT"},
                    "license_version": "LICENSE-WITHOUT-VERSION",
                    "classifier": [["License :: OSI Approved :: MIT License", "MIT License"]],
                    "warning": False,
                },
                "1.1": {
                    "license": {"full_name": "MIT License", "identifier_spdx": "MIT", "identifier": "MIT"},
                    "license_version": "LICENSE-WITHOUT-VERSION",
                    "classifier": [["License :: OSI Approved :: MIT License", "MIT License"]],
                    "warning": False,
                },
            },
            "test_2": {
                "1.0": {
                    "license": {"full_name": "MIT License", "identifier_spdx": "MIT", "identifier": "MIT"},
                    "license_version": "LICENSE-WITHOUT-VERSION",
                    "classifier": [["License :: OSI Approved :: MIT License", "MIT License"]],
                    "warning": False,
                },
                "1.1": {
                    "license": {"full_name": "MIT License", "identifier_spdx": "MIT", "identifier": "MIT"},
                    "license_version": "LICENSE-WITHOUT-VERSION",
                    "classifier": [["License :: OSI Approved :: Apache Software License", "Apache Software License"]],
                    "warning": True,
                },
            },
        }

    def test_add_package_same_package_and_version(self) -> None:
        """Test add_package with same package and version."""
        package_same_package = self.create_package(
            "test_2",
            "1.1",
            {"full_name": "MIT License", "identifier_spdx": "MIT", "identifier": "MIT"},
            "LICENSE-WITHOUT-VERSION",
            False,
            ["License :: OSI Approved :: Apache Software License", "Apache Software License"],
        )
        package_same_version = self.create_package(
            "test_2",
            "1.1",
            {"full_name": "MIT License", "identifier_spdx": "MIT", "identifier": "MIT"},
            "LICENSE-WITHOUT-VERSION",
            False,
            ["License :: OSI Approved :: Apache Software License", "Apache Software License"],
        )
        self.output_creator.add_package(package_same_package)
        self.output_creator.add_package(package_same_version)

        assert self.output_creator.file == {
            "test_1": {
                "1.0": {
                    "license": {"full_name": "MIT License", "identifier_spdx": "MIT", "identifier": "MIT"},
                    "license_version": "LICENSE-WITHOUT-VERSION",
                    "classifier": [["License :: OSI Approved :: MIT License", "MIT License"]],
                    "warning": False,
                },
                "1.1": {
                    "license": {"full_name": "MIT License", "identifier_spdx": "MIT", "identifier": "MIT"},
                    "license_version": "LICENSE-WITHOUT-VERSION",
                    "classifier": [["License :: OSI Approved :: MIT License", "MIT License"]],
                    "warning": False,
                },
            },
            "test_2": {
                "1.0": {
                    "license": {"full_name": "MIT License", "identifier_spdx": "MIT", "identifier": "MIT"},
                    "license_version": "LICENSE-WITHOUT-VERSION",
                    "classifier": [["License :: OSI Approved :: MIT License", "MIT License"]],
                    "warning": False,
                },
                "1.1": {
                    "license": {"full_name": "MIT License", "identifier_spdx": "MIT", "identifier": "MIT"},
                    "license_version": "LICENSE-WITHOUT-VERSION",
                    "classifier": [["License :: OSI Approved :: Apache Software License", "Apache Software License"]],
                    "warning": True,
                },
            },
        }

    def test_check_duplicity(self) -> None:
        """Test check_duplicity."""
        package_old = {
            "license": ["Apache License 1.1", "Apache-1.1", "Apache 1.1"],
            "license_version": "1.1",
            "warning": False,
            "classifier": ["License :: OSI Approved :: Apache Software License", "Apache Software License"],
        }

        package_new = {
            "license": ["MIT License", "MIT"],
            "license_version": "LICENSE-WITHOUT-VERSION",
            "warning": False,
            "classifier": ["License :: OSI Approved :: MIT License", "MIT License"],
        }

        package_old_empty = {
            "license": None,
            "license_version": None,
            "warning": False,
            "classifier": ["License :: OSI Approved :: Apache Software License", "Apache Software License"],
        }

        self.output_creator._check_duplicity(package_old, package_old)
        assert package_old.get("warning") is False

        self.output_creator._check_duplicity(package_old, package_new)
        assert package_old.get("warning") is True

        package_old["warning"] = False  # reset default value
        self.output_creator._check_duplicity(package_old_empty, package_old)
        assert package_old_empty.get("warning") is False
        assert package_old_empty.get("license") == ["Apache License 1.1", "Apache-1.1", "Apache 1.1"]
        assert package_old_empty.get("license_version") == "1.1"
