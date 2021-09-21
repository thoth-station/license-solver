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

"""Exception hierarchy used in the whole license-solver implementation."""


class LicenseSolverException(Exception):  # noqa: N818
    """A base license-solver exception in license-solver's exception hierarchy."""


class UnableOpenFile(LicenseSolverException):  # noqa: N818
    """An exception raised if unable to open file."""


class UnableOpenFileData(UnableOpenFile):  # noqa: N818
    """An exception raised if unable to open internal files in data/."""

    def __init__(self, txt: str = "Internal file can't be loaded"):
        """Create message."""
        super().__init__(f"{txt}")
