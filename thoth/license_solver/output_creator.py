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
from .package import Package
from typing import Dict, Any

_LOGGER = logging.getLogger(__name__)


class OutputCreator:
    """Propose of this class is to create dictionary for all packages (input)."""

    file: Dict[Any, Any] = dict()

    def add_package(self, package: Package, warning: bool = False) -> None:
        """
        Add package to dictionary.

        :param package: Package data
        :param warning: default False, if true create warning in package info
        :return: None
        """
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
                    old[index] = new[index]

                    if index == "license":
                        old["license_version"] = new["license_version"]

                elif old[index] != new[index]:
                    old["warning"] = True

    def print(self, indent: int = 4) -> None:
        """Print dictionary on STDOUT."""
        _LOGGER.debug("Print on STDOUT final json")
        print(json.dumps(self.file, indent=indent), file=sys.stdout)
