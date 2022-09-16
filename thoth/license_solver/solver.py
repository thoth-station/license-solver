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

"""Main class which work with detecting and creating output."""

import os
import sys
import json
import logging
import requests

from typing import List, Tuple, Dict, Any, Optional, Union
from os import DirEntry

from .classifiers import Classifiers
from .licenses import Licenses
from .package import Package, _detect_version_and_delete
from .json_solver import JsonSolver
from .comparator import _delete_brackets, _delete_brackets_and_content
from .output_creator import OutputCreator
from .exceptions import UnableOpenFileData

_LOGGER = logging.getLogger(__name__)


class Solver:
    """Class pass all detected files and try to detect all necessary data."""

    def __init__(self, github: bool = False) -> None:
        """Init class variables and open JSON file of license aliases."""
        self.license_dictionary: Dict[str, Any] = dict()
        self.classifiers: Classifiers = Classifiers()
        self.licenses: Licenses = Licenses()
        self.output: OutputCreator = OutputCreator(github)

        file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data", "license_dictionary.json")
        try:
            with open(file_path) as f:
                self.license_dictionary = json.load(f).get("data")
                _LOGGER.debug("File license_dictionary.json was successful loaded")
        except Exception:
            raise UnableOpenFileData

    def solve_from_file(self, input_file: Union[Dict[str, Any], str]) -> None:
        """
        Solver from file.

        :param input_file: file path
        :return: None
        """
        if isinstance(input_file, str):
            _LOGGER.debug("Parsing file: %s", input_file)
            if not self._check_if_json(input_file):
                _LOGGER.warning("Input file is not valid. SKIPPED")
                return
            # path to file
            try:
                with open(input_file) as f:
                    json_solver = JsonSolver(json.load(f), f.name)  # type: ignore[call-arg]
                    json_solver.get_info_attribute()
                    _LOGGER.debug("Loaded file %s", input_file)
            except Exception as e:
                _LOGGER.error("Broken or can't find file: %s\nerror: %s.", input_file, e)

        elif isinstance(input_file, dict):
            _LOGGER.debug("Parsing dictionary.")
            # dictionary parsing
            json_solver = JsonSolver(input_file, "dictionary_input")  # type: ignore[call-arg]

        else:
            _LOGGER.warning("Not supported type: %s. SKIPPED", type(input_file))
            return

        try:
            if json_solver is None:
                return
        except Exception:
            return

        package = Package()

        self._get_classifier_and_license(json_solver, package)
        self.output.add_package(package)

    def solve_from_directory(self, input_directory: str) -> None:
        """
        Solve from directory.

        :param input_directory: directory path
        :return: None
        """
        _LOGGER.debug("Start parsing directory %s.", input_directory)
        file_path: DirEntry  # type: ignore[type-arg]
        for file_path in os.scandir(input_directory):
            if file_path.is_file():
                self.solve_from_file(file_path.path)
            else:
                _LOGGER.debug("Subdirectory SKIPPED %s.", file_path)

    def solve_from_pypi(self, package_name: str, package_version: Optional[str]) -> None:
        """
        Solve from PyPI.

        :param package_name: package name to solver
        :param package_version: package version to solver
        :return: None
        """
        if package_version:
            url = f"https://pypi.org/pypi/{package_name}/{package_version}/json"
            response = requests.get(url, headers={"User-Agent": "license-solver"})

            if response.status_code != 200:
                _LOGGER.warning("Package %r with version %r was not found on PyPI.", package_name, package_version)
                print(f"Package {package_name} with {package_version} was not found on PyPI.", file=sys.stderr)
                return
        else:
            # get latest licenses
            url = f"https://pypi.org/pypi/{package_name}/json"
            response = requests.get(url, headers={"User-Agent": "license-solver"})

            if response.status_code != 200:
                _LOGGER.warning("Package %r was not found on PyPI.", package_name)
                print(f"Package {package_name} was not found on PyPI.", file=sys.stderr)
                return

        # convert to dictionary
        res = json.loads(response.text)
        # solver like file
        self.solve_from_file(res)
        self.solve_from_file(res.get("info"))

    def _get_classifier_and_license(self, json_file: JsonSolver, package: Package) -> None:
        """
        Get classifier and license groups and save them to parameter package.

        :param json_file: json class which hold data from file
        :param package: class package which will hold all package data
        :return: None
        """
        package.set_file_path(json_file.path)

        package.set_package_name(json_file.get_package_name())
        package.set_version(json_file.get_package_version())

        license_name = json_file.get_license_name()
        package.set_license(self._get_license_group(license_name))

        classifier_name = json_file.get_classifier_name()
        package.set_classifier(self._get_classifier_group(classifier_name))

    def _get_license_group(self, license_name: Optional[str]) -> Tuple[List[str], bool]:
        """
        Search for a group of entered license name.

        :param license_name: name of license to find in class license_list
        :return: Tuple[List[str], bool]:
        """
        # undetected license
        if license_name is None:
            return list(["UNDETECTED"]), False

        # UNKNOWN license name
        if license_name.lower() == "unknown":
            return list(["UNKNOWN"]), False

        # pass license list
        for lic_li in self.licenses.licenses_list:
            lic_li_lower = [x.lower() for x in lic_li]
            if (
                license_name.lower() in lic_li_lower
                or _delete_brackets(license_name).lower() in lic_li_lower
                or _delete_brackets_and_content(license_name).lower() in lic_li_lower
            ):
                return lic_li, True

        # try to found license without version or license in dictionary
        for lic_li in self.licenses.licenses_list:
            license_name_no_version, _ = _detect_version_and_delete(lic_li[len(lic_li) - 1])

            if self.license_dictionary.get(license_name.lower()) in lic_li:
                # license found in license dictionary
                _license = self.license_dictionary.get(license_name.lower())
                _license_li = [x for x in self.licenses.licenses_list if _license in x][0]
                return _license_li, True
            elif license_name_no_version == license_name:
                return list([license_name]), True

        return list(["UNDETECTED"]), False

    def _get_classifier_group(self, classifier_name: Optional[List[str]]) -> Optional[List[str]]:
        """
        Search for a group of entered classifier name.

        :param classifier_name: name of license to find in class classifier list
        :return: None
        """
        if classifier_name is None:
            return None

        cla_li: List[str]
        for cla_li in self.classifiers.classifiers_list:
            # lowercase lists and compare
            cla_li_lower = [x.lower() for x in cla_li.copy()]
            classifier_name_lower = [x.lower() for x in classifier_name.copy()]

            if list(set(cla_li_lower) & set(classifier_name_lower)):
                return cla_li

        return None

    def print_output(self, indent: int = -1) -> None:
        """Print final output on STDOUT."""
        self.output.print(indent)

    def save_output(self, file_name: str, indent: int = -1) -> None:
        """Save solver result to JSON."""
        f = open(file_name, "w")
        if indent < 0:
            f.write(json.dumps(self.output.file))
        else:
            f.write(json.dumps(self.output.file, indent=indent))
        f.close()

    def get_output_dict(self, **kw: Any) -> Dict[str, Any]:
        """Return dictionary from OutputCreator class."""
        condition = True if kw["package_name"] and kw["package_version"] else False
        return (  # type: ignore[no-any-return]
            self.output.file[kw["package_name"]][kw["package_version"]] if condition else self.output.file
        )

    @staticmethod
    def get_empty_dict() -> Dict[str, Any]:
        """Return empty dictionary for license."""
        return {
            "license": {
                "full_name": "UNDETECTED",
                "identifier": "UNDETECTED",
                "identifier_spdx": "UNDETECTED",
            },
            "license_version": "UNDETECTED",
            "warning": True,
        }

    @staticmethod
    def _check_if_json(input_file: str) -> bool:
        """Check if input file is JSON type."""
        if not input_file.endswith(".json"):
            _LOGGER.warning("File %s is not JSON type. SKIPPED", input_file)
            return False
        return True
