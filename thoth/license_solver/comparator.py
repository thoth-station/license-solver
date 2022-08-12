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

"""A Class compare classifier and license."""

import os
import re
import yaml
import json
import logging
import urllib.request
import urllib.error
from typing import List, Any, Dict
from .package import Package

_LOGGER = logging.getLogger(__name__)


def _delete_brackets(license_list: str) -> str:
    return re.sub(r"(\(?)(\)?)", "", license_list).strip()


def _delete_brackets_and_content(license_list: str) -> str:
    return re.sub(r"\(.*?\)", "", license_list).strip()


class Comparator:
    """Class Comparator compare classifiers and licenses."""

    def __init__(self, github: bool = False) -> None:
        """
        Init class variables.

        :param: github: check license with github repository
        :return: None
        """
        self.github: bool = github
        self._comparator_dictionary: Dict[str, Any] = self.open_dictionary()

    def open_dictionary(self) -> Any:
        """
        Open directory with dictionary for Comparator.

        :return: yaml
        """
        file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data", "comparator_dictionary.yaml")
        with open(file_path) as f:
            try:
                return yaml.safe_load(f)
            except yaml.YAMLError:
                _LOGGER.warning("Can't open data/comparator_dictionary.yaml or broken file")
                raise yaml.YAMLError

    def cmp(self, package: Package) -> bool:
        """
        Compare License and Classifier from package data.

        :param package: Package from input
        :return: True if match, False if not
        """
        license_name = package.license
        classifier_name = package.classifier

        debug_tab = 10 * "\t"

        if not license_name or not classifier_name:
            return True

        license_list = [license_name["full_name"], license_name["identifier_spdx"], license_name["identifier"]]

        for x in classifier_name:

            _LOGGER.debug("Compare license and classifier:\n" "%s%s\n" "%s%s", debug_tab, license_name, debug_tab, x)

            if (
                list(set(license_list) & set(x))
                or self.search_in_dictionary(license_list, x)
                or classifier_name[0][0] == "UNDETECTED"
                or license_list[0] == "UNKNOWN"
                or license_list[0].lower() == "the unlicense"
            ):
                _LOGGER.debug("Found match or alias")

                return True if not self.github else self.check_github(package)

        _LOGGER.debug("No match")
        return False

    def check_github(self, package: Package) -> bool:
        """
        Compare github license with PyPI license.

        :param package: name of package to check
        :return: True if match, False if not
        """
        prescription = self._get_prescription(package.name)

        if prescription is None:
            _LOGGER.warning("Failed to check github license for %s", package.name)
            return True

        link = prescription["units"]["wraps"][0]["run"]["justification"][0]["link"]
        owner, repo = link.split("/")[-2:]
        url = f"https://api.github.com/repos/{owner}/{repo}/license"
        data_api_github = json.loads(urllib.request.urlopen(url).read().decode())

        return True if data_api_github["license"]["spdx_id"] in package.license["identifier_spdx"] else False

    def search_in_dictionary(self, license_name: List[str], classifier: List[str]) -> bool:
        """
        Search for alias in data/comparator_dictionary.yaml.

        :param license_name: License to compare with classifier
        :param classifier: Classifier to compare with license
        :return: True if found match, False if not
        """
        if len(license_name) == 0:
            return False

        if (
            classifier[0] == "UNDETECTED" and self._comparator_dictionary["classifier"].get(classifier[0]) is not None
        ) or (
            classifier[0] != "UNDETECTED" and self._comparator_dictionary["classifier"].get(classifier[1]) is not None
        ):
            for x in self._comparator_dictionary["classifier"].get(classifier[1]):
                if x == license_name[0]:
                    return True

        return False

    def _get_prescription(self, package_name: str) -> Any:
        """
        Get prescription from https://github.com/thoth-station/prescriptions.

        :param package_name: Package name
        :return: None if method failed, yaml if prescription is found
        """
        name = re.sub("[^a-zA-z0-9]", "-", package_name)
        url = "https://raw.githubusercontent.com/thoth-station/prescriptions/master/prescriptions/"

        if len(name) == 1:
            url += f"{name}/gh_link.yaml"
        elif len(name) == 2:
            url += f"{name[:2]}/gh_link.yaml"
        else:
            url += f"{name[:2]}_/{name}/gh_link.yaml"

        try:
            r = urllib.request.urlopen(url).read().decode()  # get webpage data
            text = yaml.safe_load(r)
        except urllib.error.HTTPError as e:
            _LOGGER.warning("Failed to download prescription: %s", e)
            text = None
        except yaml.YAMLError as e:
            _LOGGER.warning("Failed open downloaded prescription: %s", e)
            text = None

        return text
