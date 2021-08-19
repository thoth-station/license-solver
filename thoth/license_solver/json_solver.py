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

"""A class for work with loaded json files."""

import attr
from attr import attrib
import logging
from typing import Dict, Any, Union, Optional, List

_LOGGER = logging.getLogger("thoth.license_solver.json_solver")


@attr.s(slots=True)
class JsonSolver:
    """Class JsonSolver extend class LicenseSolver, help inquiry json data from metadata."""

    json_file = attrib(type=Dict[str, Any])
    path = attrib(type=str)

    def get_package_name(self) -> Optional[Any]:
        """Get package name from metadata."""
        try:
            return self.json_file["result"]["tree"][0].get("package_name")
        except Exception:
            _LOGGER.debug("Can't detect package name from input file")
            return None

    def get_package_version(self) -> Optional[Any]:
        """Get package version from metadata."""
        try:
            return self.json_file["result"]["tree"][0].get("package_version")
        except Exception:
            _LOGGER.debug("Can't detect package version from input file")
            return None

    def get_license_name(self) -> Optional[Any]:
        """Get license name from metadata."""
        try:
            return self.json_file["result"]["tree"][0]["importlib_metadata"]["metadata"].get("License")
        except Exception:
            _LOGGER.debug("Can't detect license_name from input file")
            return None

    def get_classifier_name(self) -> Union[List[Any], Any, None]:
        """Get classifier name from metadata."""
        try:
            return self.json_file["result"]["tree"][0]["importlib_metadata"]["metadata"].get("Classifier")
        except Exception:
            _LOGGER.debug("Can't detect license_name from input file")
            return None

    def get_errors(self) -> bool:
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
            _LOGGER.debug("Metadata from file have error (skipped)")
            return False
