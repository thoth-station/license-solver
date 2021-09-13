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

"""File is proposed for creating Package objects."""

import re
import yaml
import os
import logging
from typing import Union, Tuple, List, Any, Optional

_LOGGER = logging.getLogger(__name__)


def _detect_version_and_delete(string: str) -> Union[Tuple[str, str], Tuple[str, None]]:
    """
    Delete version of license from string.

    :returns tuple
        - license name without version - first output
        - version - second output.
    """
    regex = r"( v\d+\.| \d| version |, version)(\.\d|\d)*[\w]*"

    try:
        find = re.search(regex, string)
        if find:
            return re.sub(regex, "", string).strip(), find.group(0).strip()
        else:
            return re.sub(regex, "", string).strip(), None
    except Exception:
        return re.sub(regex, "", string).strip(), None


class Package:
    """Object which store values metadata."""

    name: str = ""
    version: str = ""
    license: List[str] = list()
    license_version: str = ""
    classifier: List[List[str]] = list()
    file_path: str = ""

    def set_package_name(self, package_name: Optional[Any]) -> None:
        """Set package name."""
        if type(package_name) is str:
            self.name = package_name
            _LOGGER.debug("Set name package: %s", package_name)
        else:
            _LOGGER.debug("Unsuccessful set name package")

    def set_version(self, package_version: Optional[Any]) -> None:
        """Set version of package name."""
        if type(package_version) is str:
            self.version = package_version
            _LOGGER.debug("Set name package: %s", package_version)
        else:
            _LOGGER.debug("Unsuccessful set version package")

    def set_license(self, license_name: Tuple[List[str], bool]) -> None:
        """Set type of license."""
        file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data", "license_without_versions.yaml")
        with open(file_path) as f:
            data = yaml.safe_load(f)
            licenses_without_version = data["license-no-versions"]

        if len(license_name[0]) > 1:
            if license_name[0][0] in licenses_without_version:
                self.license = license_name[0]
                self.set_license_version("LICENSE-WITHOUT-VERSION")
                _LOGGER.debug("Set license %s and version %s", license_name[0], "LICENSE-WITHOUT-VERSION")
            elif license_name[1]:
                _license_name_no_version, _license_version = _detect_version_and_delete(
                    license_name[0][len(license_name[0]) - 1]
                )
                self.license = license_name[0]

                if _license_version is None:
                    self.set_license_version("UNDETECTED")
                    _LOGGER.debug("Set license %s and version %s", license_name[0], "UNDETECTED")
                else:
                    self.set_license_version(_license_version)
                    _LOGGER.debug("Set license %s and version %s", license_name[0], _license_version)
            else:
                self.license = license_name[0]
                self.set_license_version("UNDETECTED")
                _LOGGER.debug("Set license %s and version %s", license_name[0], "UNDETECTED")
        elif len(license_name[0]) == 1:
            self.license = license_name[0]
            self.set_license_version("UNDETECTED")
            _LOGGER.debug("Set license %s and version %s", license_name[0], "UNDETECTED")
        else:
            self.license = list(["UNKNOWN"])
            self.set_license_version("UNDETECTED")
            _LOGGER.debug("Set license %s and version %s", list(["UNKNOWN"]), "UNDETECTED")

    def set_license_version(self, license_version: str) -> None:
        """Set version of license."""
        self.license_version = license_version

    def set_classifier(self, classifier: Optional[List[str]]) -> None:
        """Set classifier."""
        if classifier is None:
            return

        if len(self.classifier) == 0:
            self.classifier = list([classifier])
        else:
            if not (classifier in self.classifier):
                self.classifier.append(classifier)

    def set_file_path(self, path: str) -> None:
        """Set file path."""
        self.file_path = path

    def print(self) -> None:
        """Print class property on STDOUT."""
        print(
            f"package:\t\t {self.name}\n"
            f"version:\t\t {self.version}\n"
            f"license:\t\t {self.license}\n"
            f"license_version: {self.license_version}\n"
            f"classifier:\t\t {self.classifier}\n"
            f"file_path:\t\t {self.file_path}"
        )
