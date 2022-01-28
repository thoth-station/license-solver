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

    def get_info_attribute(self) -> None:
        """Get info from metadata."""
        res = self.json_file.get("info")
        if res is not None:
            self.json_file = res  # type: ignore[assignment]

    def get_package_name(self) -> Optional[Any]:
        """Get package name from metadata."""
        return self.json_file.get("Name") or self.json_file.get("name")

    def get_package_version(self) -> Optional[Any]:
        """Get package version from metadata."""
        return self.json_file.get("Version") or self.json_file.get("version")

    def get_license_name(self) -> Optional[Any]:
        """Get license name from metadata."""
        return self.json_file.get("License") or self.json_file.get("license")

    def get_classifier_name(self) -> Union[List[Any], Any, None]:
        """Get classifier name from metadata."""
        return self.json_file.get("Classifier") or self.json_file.get("classifiers")
