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

from thoth.license_solver.classifiers import Classifiers
from thoth.license_solver.exceptions import UnableOpenFileData


class TestClassifier:
    """Test classifier."""

    classifier: Classifiers = Classifiers()

    def test_wrong_file_path(self) -> None:
        """Test loading file and test with wrong file path."""
        with pytest.raises(UnableOpenFileData):
            self.classifier.load_data(file_path="wrong_path")

    def test_init_variables(self) -> None:
        """Test if variables are initialized."""
        assert self.classifier.classifiers, "Failed to load JSON data"
        assert self.classifier.classifiers_list

    def test_extract_name(self) -> None:
        """Test extracting classifier name."""
        classifier_txt = "License :: OSI Approved :: MIT License"
        assert self.classifier._extract_name(classifier_txt) == "MIT License", "extract_name does not work properly"
        assert self.classifier._extract_name("") == ""

    def test_extract_abbreviation(self):
        """Text extracting abbreviation."""
        classifier_txt_no_abbreviation = "License :: OSI Approved :: MIT License"
        classifier_txt_with_abbreviation = "License :: OSI Approved :: Mozilla Public License 1.0 (MPL)"

        assert (
            self.classifier._extract_abbreviation(classifier_txt_no_abbreviation) == list()
        ), "Example does not have abbreviation"

        assert self.classifier._extract_abbreviation(classifier_txt_with_abbreviation) == (
            ["MPL"]
        ), "Example does have abbreviation, but no found"
