#!/usr/bin/env python3
# solver-license-job
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

"""A class for work with loaded json files."""

import attr


@attr.s
class JsonSolver:
    """Class JsonSolver extend class LicenseSolver, help inquiry json data from metadata."""

    json_file: dict = attr.ib()
    path: object = attr.ib()

    def get_package_name(self):
        """Get package name from metadata."""
        try:
            return self.json_file["result"]["tree"][0].get("package_name")
        except Exception:
            return None

    def get_package_version(self):
        """Get package version from metadata."""
        try:
            return self.json_file["result"]["tree"][0].get("package_version")
        except Exception:
            return None

    def get_license_name(self):
        """Get license name from metadata."""
        try:
            return self.json_file["result"]["tree"][0]["importlib_metadata"]["metadata"].get("License")
        except Exception:
            return None

    def get_classifier_name(self):
        """Get classifier name from metadata."""
        try:
            return self.json_file["result"]["tree"][0]["importlib_metadata"]["metadata"].get("Classifier")
        except Exception:
            return None

    def get_errors(self):
        """
        Check if errors occurred return True.

        result->errors
        result->unparsed
        result->unresolved
        """
        try:
            return not (
                self.json_file["result"].get("errors")
                or self.json_file["result"].get("unparsed")
                or self.json_file["result"].get("unresolved")
            )
        except Exception:
            return False
