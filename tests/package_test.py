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

"""Tests related to class Package."""

from thoth.license_solver.package import Package


class TestPackage:
    """Test Package."""

    package: Package = Package()

    def test_set_package_name(self) -> None:
        """Test set_package_name function."""
        self.package.set_package_name(None)
        assert self.package.name == ""

        self.package.set_package_name("name")
        assert self.package.name == "name"

        self.package.set_package_name("name_2")
        assert self.package.name == "name_2"

    def test_set_version(self) -> None:
        """Test set_version function."""
        self.package.set_version(None)
        assert self.package.version == ""

        self.package.set_version("1.0")
        assert self.package.version == "1.0"

        self.package.set_version("1.1")
        assert self.package.version == "1.1"

    def test_set_license(self) -> None:
        """Test set_license function."""
        # license found in license_without_version dictionary
        license_without_version = (["MIT License", "MIT", "MIT"], True)
        self.package.set_license(license_without_version)
        assert (
            self.package.license == {"full_name": "MIT License", "identifier_spdx": "MIT", "identifier": "MIT"}
            and self.package.license_version == "LICENSE-WITHOUT-VERSION"
        )

        # license extract version
        license_with_version = (["Apache License 1.1", "Apache-1.1", "Apache 1.1"], True)
        self.package.set_license(license_with_version)
        assert (
            self.package.license
            == {"full_name": "Apache License 1.1", "identifier_spdx": "Apache-1.1", "identifier": "Apache 1.1"}
            and self.package.license_version == "1.1"
        )

        # license without version
        license_with_version = (["Apache License", "Apache", "Apache"], False)
        self.package.set_license(license_with_version)
        assert (
            self.package.license == {"full_name": "Apache License", "identifier_spdx": "Apache", "identifier": "Apache"}
            and self.package.license_version == "UNDETECTED"
        )

        # test license without version
        license_without_version = (list(["LGPL"]), True)
        self.package.set_license(license_without_version)
        assert (
            self.package.license == {"full_name": "LGPL", "identifier_spdx": "UNDETECTED", "identifier": "UNDETECTED"}
            and self.package.license_version == "UNDETECTED"
        )

        # undetected license
        self.package.set_license((list(), False))
        assert (
            self.package.license
            == {"full_name": "UNDETECTED", "identifier": "UNDETECTED", "identifier_spdx": "UNDETECTED"}
            and self.package.license_version == "UNDETECTED"
        )
        self.package.set_license((list(["AAA", "AAA", "AAA"]), True))
        assert self.package.license_version == "UNDETECTED"

    def test_set_license_version(self) -> None:
        """Test set_license_version function."""
        self.package.set_license_version("1")
        assert self.package.license_version == "1"

        self.package.set_license_version("2")
        assert self.package.license_version == "2"

    def test_set_classifier(self) -> None:
        """Test set_classifier function."""
        # test None
        self.package.set_classifier(None)
        assert self.package.classifier == list([["UNDETECTED"]])
        # insert classifier
        self.package.classifier = list()
        self.package.set_classifier(["License :: OSI Approved :: MIT License", "MIT License"])
        assert self.package.classifier == [["License :: OSI Approved :: MIT License", "MIT License"]]
        # try to insert same classifier
        self.package.set_classifier(["License :: OSI Approved :: MIT License", "MIT License"])  # append same classifier
        assert self.package.classifier == [["License :: OSI Approved :: MIT License", "MIT License"]]
        # insert another classifier
        self.package.set_classifier(["License :: OSI Approved :: Apache Software License", "Apache Software License"])
        assert self.package.classifier == [
            ["License :: OSI Approved :: MIT License", "MIT License"],
            ["License :: OSI Approved :: Apache Software License", "Apache Software License"],
        ]

    def test_set_file_path(self) -> None:
        """Test set_file_path function."""
        self.package.set_file_path("path_1")
        assert self.package.file_path == "path_1"

        self.package.set_file_path("path_2")
        assert self.package.file_path == "path_2"
