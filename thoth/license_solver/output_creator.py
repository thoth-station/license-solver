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

"""Class create output dictionary."""

import json
import sys
import logging
from .comparator import Comparator
from .package import Package
from typing import Dict, Any

_LOGGER = logging.getLogger(__name__)


class OutputCreator:
    """Propose of this class is to create dictionary for all packages (input)."""

    def __init__(self, github: bool = False) -> None:
        """
        Init variables for OutputCreator.

        :param github:
        """
        self.file: Dict[Any, Any] = dict()
        self.comparator: Comparator = Comparator(github)

    def add_package(self, package: Package) -> None:
        """
        Add package to dictionary.

        :param package: Package data
        :return: None
        """
        warning = False

        # save only package with name and version
        if package.name and package.version:
            if not self.comparator.cmp(package):
                warning = True

            package_data: Dict[str, Any] = {
                "license": package.license,
                "license_version": str(package.license_version),
                "classifier": package.classifier,
            }

            if warning:
                package_data["warning"] = True
            else:
                package_data["warning"] = False

            if self.file.get(package.name) is None:
                self.file[package.name] = {package.version: package_data}
            else:
                if self.file[package.name].get(package.version) is None:
                    self.file[package.name][package.version] = package_data
                else:
                    self._check_duplicity(self.file[package.name].get(package.version), package_data)

            _LOGGER.debug("Add package to OutputCreator: %s", package_data)

        else:
            _LOGGER.debug("The file %s has no package name or version. SKIPPED to create OUTPUT", package.file_path)

    @staticmethod
    def _check_duplicity(old: Dict[str, Any], new: Dict[str, Any]) -> None:
        """
        Check version duplicity, if they don't match create warning in dict.

        :param old: package in class dictionary
        :param new: new package witch want to be added
        :return: None
        """
        if old == new or old["warning"]:
            return
        else:
            for index in old:
                if old[index] is None and old[index] != new[index]:
                    if index != "license_version":
                        old[index] = new[index]

                    if index == "license":
                        old["license_version"] = new["license_version"]

                    _LOGGER.debug("Update package information %s to %s", index, new[index])

                elif old[index] != new[index]:
                    _LOGGER.debug("Found not same duplicity set warning=True")
                    old["warning"] = True

    def is_empty(self) -> bool:
        """Check if variable file is empty."""
        return True if not self.file else False

    def print(self, indent: int = -1) -> None:
        """Print dictionary on STDOUT."""
        _LOGGER.debug("Print on STDOUT final json")
        if indent < 0:
            print(json.dumps(self.file), file=sys.stdout)
        else:
            print(json.dumps(self.file, indent=indent), file=sys.stdout)
