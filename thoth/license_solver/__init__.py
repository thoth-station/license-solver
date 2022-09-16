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

"""Init package."""

from .solver import Solver
from typing import Dict, Any, List, Union, Optional

__title__ = "license-solver"
__version__ = "0.1.5"
__author__ = "Viliam Podhajecky <vpodhaje@redhat.com>"


def detect_license(
    input_data: Union[Dict[str, Any], str, List[str], List[Dict[str, Any]]],
    package_name: Optional[str] = None,
    package_version: Optional[str] = None,
    raise_on_error: bool = True,
    github_check: bool = False,
) -> Dict[str, Any]:
    """Detect license with license-solver."""
    condition = True if package_name and package_version else False

    try:
        license_solver = Solver(github_check)

        if isinstance(input_data, dict) or isinstance(input_data, str):
            license_solver.solve_from_file(input_data)
        elif isinstance(input_data, dict):
            for enter in input_data:
                license_solver.solve_from_file(enter)

        return (
            license_solver.get_output_dict(package_name=package_name, package_version=package_version)
            if condition
            else license_solver.get_output_dict()
        )

    except Exception:
        if raise_on_error:
            raise Exception

        if condition:
            return Solver.get_empty_dict()
        else:
            return {}


__all__ = [
    "__version__",
    "detect_license",
]
