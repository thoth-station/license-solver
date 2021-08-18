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

"""Main class witch work with detecting and creating output."""

import os
import json
import attr
import logging
from typing import List, Tuple, Union, Dict, Any, Optional
from .classifiers import Classifiers
from .licenses import Licenses
from .package import Package, _detect_version_and_delete
from .json_solver import JsonSolver
from .comparator import Comparator, _delete_brackets, _delete_brackets_and_content
from .output_creator import OutputCreator

_LOGGER = logging.getLogger(__name__)


@attr.s(slots=True)
class Solver:
    """Class pass all detected files and try to detect all necessary data."""

    license_dictionary: Dict[str, Any] = attr.ib(init=False)
    _files_list: List[str] = list()

    classifiers: Classifiers = Classifiers()
    licenses: Licenses = Licenses()
    output: OutputCreator = OutputCreator()

    def __attrs_post_init__(self) -> None:
        """Open JSON file of license aliases."""
        file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data/license_dictionary.json")
        try:
            with open(file_path) as f:
                self.license_dictionary = json.load(f).get("data")
                _LOGGER.debug("File license_dictionary.json was successful loaded")
        except OSError:
            raise OSError

    def create_file(self) -> None:
        """
        Pass all input files and create output, witch will be printed on STDOUT.

        :return: None
        """
        comparator = Comparator()
        _LOGGER.debug("Start parsing file list")
        for file_path in self._files_list[:]:
            _LOGGER.debug(f"Parsing file: {file_path}")
            # pass all listed metadata
            try:
                with open(file_path) as f:
                    json_solver = JsonSolver(json.load(f), f.name)  # type: ignore[call-arg]
                    _LOGGER.debug(f"Loaded file {file_path}")
            except Exception as e:
                _LOGGER.error(f"Broken or can't find file: {file_path} error: {e}")
                exit(1)

            package = Package()
            self.get_classifier_and_license(json_solver, package)

            # save only package with name and version
            if package.name and package.version:
                if package.license and package.classifier:
                    if comparator.cmp(package):
                        # no warning
                        self.output.add_package(package)
                    else:
                        # set warning
                        self.output.add_package(package, warning=True)
                        pass
                else:
                    # no need to compare license and classifier
                    self.output.add_package(package)

        # print result to STDOUT
        self.output.print()

    def get_classifier_and_license(self, json_file: JsonSolver, package: Package) -> None:
        """
        Get classifier and license groups and save them to parameter package.

        :param json_file: json class witch hold data from file
        :param package: class package witch will hold all package data
        :return: None
        """
        package.set_file_path(json_file.path)

        package.set_package_name(json_file.get_package_name())
        package.set_version(json_file.get_package_version())

        license_name = json_file.get_license_name()
        package.set_license(self.get_license_group(license_name))

        classifier_name = json_file.get_classifier_name()
        package.set_classifier(self.get_classifier_group(classifier_name))

    def get_license_group(self, license_name: Optional[Any]) -> Tuple[List[str], bool]:
        """
        Search for a group of entered license name.

        :param license_name: name of license to find in class license_list
        :return: Tuple[List[str], bool]:
        """
        # undetected license
        if license_name is None:
            return list(["UNKNOWN"]), False

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

        return list(), False

    def get_classifier_group(self, classifier_name: Union[List[Any], Any, None]) -> Optional[Any]:
        """
        Search for a group of entered classifier name.

        :param classifier_name: name of license to find in class classifier list
        :return: None
        """
        if classifier_name is None:
            return None

        for cla_li in self.classifiers.classifiers_list:
            if list(set(cla_li) & set(classifier_name)):
                return cla_li

        return None

    def get_file(self, file: str) -> None:
        """
        Add file to file_list.

        :param file: path to file
        :return: None
        """
        if os.path.isfile(file) and file.lower().endswith(".json"):
            self._files_list.append(file)
        else:
            _LOGGER.warning("wrong format you can insert only .json file: ", file)

    def get_dir_files(self, directory: str) -> None:
        """
        Create list of all files in directory.

        :param directory: path to directory
        :return: None
        """
        if os.path.isdir(directory):
            _LOGGER.debug("Creating list of file from directory")
            for f in os.listdir(directory):
                full_path = os.path.join(directory, f)
                if full_path.lower().endswith(".json"):
                    self._files_list.append(full_path)
                else:
                    _LOGGER.warning("wrong format you can insert only .json SKIPPED: ", f)
        else:
            _LOGGER.warning("invalid path to directory")
