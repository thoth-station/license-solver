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


"""A class create easier way to handle with license-solver output."""

from typing import Dict, Any
import attr


@attr.s(slots=True)
class SolverLicense:
    """Class work with output from license_solver."""

    data = attr.ib(type=Dict[str, Any])

    def get_all(self, package_name: str, package_version: str) -> Dict[str, Any]:
        """Get all necessary data for license."""
        try:
            return {
                "license": self.get_license_full_name(package_name, package_version),
                "license_identifier": self.get_license_idetentifier(package_name, package_version),
                "license_version": self.get_license_version(package_name, package_version),
                "warning": self.get_warning(package_name, package_version),
            }
        except Exception:
            return {
                "license": "UNDETECTED",
                "license_identifier": "UNDETECTED",
                "license_version": "UNDETECTED",
                "warning": True,
            }

    def get_license_full_name(self, package_name: str, package_version: str) -> str:
        """Get license name for package with specific package version."""
        try:
            result: str = self.data[package_name][package_version]["license"][0]
            return result

        except Exception:
            return "UNDETECTED"

    def get_license_idetentifier(self, package_name: str, package_version: str) -> str:
        """Get license name for package with specific package version."""
        try:
            result: str = self.data[package_name][package_version]["license"][1]
            return result
        except Exception:
            return "UNDETECTED"

    def get_license_version(self, package_name: str, package_version: str) -> str:
        """Get license version for package with specific package version."""
        try:
            result: str = self.data[package_name][package_version]["license_version"]
            return result
        except Exception:
            return "UNDETECTED"

    def get_warning(self, package_name: str, package_version: str) -> bool:
        """Get warning for package with specific package version."""
        try:
            result: bool = self.data[package_name][package_version]["warning"]
            return result
        except Exception:
            return True
