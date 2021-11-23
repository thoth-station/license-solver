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

from typing import Dict, Any, List, Union

__title__ = "license-solver"
__version__ = "0.1.0"
__author__ = "Viliam Podhajecky <vpodhaje@redhat.com>"


def detect_license(
    input_data: Union[Dict[str, Any], str, List[str], List[Dict[str, Any]]], raise_on_error: bool = True
) -> Dict[str, Any]:
    """Run license-solver from thoth-solver."""
    try:
        license_solver = Solver()

        if type(input_data) == dict or type(input_data) == str:
            license_solver.solve_from_file(input_data)
        elif type(input_data) == list:
            for enter in input_data:
                license_solver.solve_from_file(enter)

        return license_solver.get_output_dict()

    except Exception:
        if raise_on_error:
            raise Exception

        return Solver().get_empty_dict()


__all__ = ["detect_license"]
