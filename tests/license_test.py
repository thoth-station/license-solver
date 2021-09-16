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

"""Tests related to class Licenses."""
import pytest

from thoth.license_solver.exceptions import UnableOpenFileData
from thoth.license_solver.licenses import Licenses


class TestLicense:
    """Test license."""

    licenses: Licenses = Licenses()

    def test_wrong_file_path(self) -> None:
        """Test loading file and test with wrong file path."""
        with pytest.raises(UnableOpenFileData):
            self.licenses.load_data(file_path="wrong_path")

    def test_init_variables(self) -> None:
        """Test if variables are initialized."""
        assert self.licenses.json_data, "Failed to load JSON data"
        assert self.licenses.licenses
        assert self.licenses.licenses_list

    def test_extract(self):
        """Test extract."""
        self.licenses.json_data = {"licenses": {"aa": "a"}}

        self.licenses._extract()
