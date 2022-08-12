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

"""Test related to class Comparator."""

from thoth.license_solver.comparator import Comparator
from thoth.license_solver.package import Package


class TestComparator:
    """Test Comparator."""

    comparator: Comparator = Comparator(False)

    # tests related to Compare().cmp()
    def test_cmp(self) -> None:
        """Test compare function in Comparator class."""
        package_1 = Package()
        assert self.comparator.cmp(package_1), "Empty package return true, because there is nothing to compare"
        package_1.set_license((["Apache License 1.1", "Apache-1.1", "Apache 1.1"], True))
        package_1.set_classifier(["License :: OSI Approved :: Apache Software License", "Apache Software License"])
        assert self.comparator.cmp(package_1), "Not matched apache license and classifier"

        package_2 = Package()
        package_2.set_license((["MIT License", "MIT", "MIT"], True))
        package_2.set_classifier(["License :: OSI Approved :: MIT License", "MIT License"])
        assert self.comparator.cmp(package_2), "Not matched MIT license and classifier"

        # test wrong license and classifier
        package_3 = Package()
        package_3.set_license((["MIT License", "MIT", "MIT"], True))
        package_3.set_classifier(["License :: OSI Approved :: Apache Software License", "Apache Software License"])
        assert self.comparator.cmp(package_3) is False, "License and Classifier can't match"

    def test_cmp_missing(self) -> None:
        """Test compare function in Comparator class and check result for missing license or classifier or both."""
        package_1 = Package()
        package_1.set_license((["Apache License 1.1", "Apache-1.1", "Apache 1.1"], True))
        assert self.comparator.cmp(package_1), "Must return true, because there is nothing to compare"
        # del package_1

        package_2 = Package()
        package_2.set_classifier(["License :: OSI Approved :: MIT License", "MIT License"])
        assert self.comparator.cmp(package_2), "Must return true, because there is nothing to compare"

    # tests related to Compare().search_in_dictionary()
    def test_search_in_dictionary(self) -> None:
        """Test function search_in_dictionary."""
        license_name = ['BSD 4-Clause "Original" or "Old" License']
        license_name_not_valid = ["Not Valid", "NoV"]
        classifier = ["License :: OSI Approved :: BSD License", "BSD License"]
        classifier_not_valid = ["Not valid", "Not Valid"]

        assert self.comparator.search_in_dictionary(license_name, classifier), "License was not found in dictionary"
        assert (
            self.comparator.search_in_dictionary(license_name_not_valid, classifier) is False
        ), "Can't match classfier with license"
        assert (
            self.comparator.search_in_dictionary(license_name, classifier_not_valid) is False
        ), "Classifier cant be find because is not defined in dictionary file"

    def test_search_in_dictionary_missing(self) -> None:
        """Test missing data/input in search_in_dictionary in Comparator."""
        assert self.comparator.search_in_dictionary(list(), list()) is False, "Nothing to found in license dictionary"
