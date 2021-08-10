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

"""A Class compare classifier and license."""

import re
import yaml
import attr
import logging
from typing import List, Any, Dict
from license_solver.package import Package

_LOGGER = logging.getLogger(__name__)


def _delete_brackets(license_list: str) -> str:
    return re.sub(r"(\(?)(\)?)", "", license_list).strip()


def _delete_brackets_and_content(license_list: str) -> str:
    return re.sub(r"\(.*?\)", "", license_list).strip()


@attr.s(slots=True)
class Comparator:
    """Class Comparator compare classifiers and licenses."""

    _comparator_dictionary: Dict[str, Any] = attr.ib(init=False)

    def __attrs_post_init__(self) -> None:
        """Open dictionary for comparing license and classifier."""
        with open("data/comparator_dictionary.yaml", "r") as f:
            try:
                self._comparator_dictionary = yaml.safe_load(f)
            except yaml.YAMLError:
                _LOGGER.warning("Can't open data/comparator_dictionary.yaml or broken file")
                exit(1)

    def cmp(self, package: Package) -> bool:
        """
        Compare License and Classifier from package data.

        :param package: Package from input
        :return: True if match, False if not
        """
        _license = package.license
        _classifier = package.classifier

        if not _license or not _classifier:
            return True

        for x in _classifier:
            if (
                list(set(_license) & set(x))
                or self.search_in_dictionary(_license, x)
                or _license[0] == "UNKNOWN"
                or _license[0].lower() == "the unlicense"
            ):
                # print("Match ", list(set(_license) & set(_classifier[0])), "\n") # DEBUG
                return True

        # print("Warning\n")
        return False

    def search_in_dictionary(self, license_name: List[str], classifier: List[str]) -> bool:
        """
        Search for alias in data/comparator_dictionary.yaml.

        :param license_name: License to compare with classifier
        :param classifier: Classifier to compare with license
        :return: True if found match, False if not
        """
        if len(license_name) == 0:
            return False

        if self._comparator_dictionary["classifier"].get(classifier[1]) is not None:
            for x in self._comparator_dictionary["classifier"].get(classifier[1]):
                if x == license_name[0]:
                    return True

        return False
