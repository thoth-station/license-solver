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

"""Main class witch work with detecting and creating output."""

import os
import sys
import json
from attr import attrs
from license_solver.classifiers import Classifiers
from license_solver.licenses import Licenses
from license_solver.package import Package, _detect_version_and_delete
from license_solver.json_solver import JsonSolver
from license_solver.comparator import Comparator, _delete_brackets, _delete_brackets_and_content
from license_solver.output_creator import OutputCreator

COUNTER_DEBUG = 0


@attrs
class LicenseSolver:
    """Class pass all detected files and try to detect all necessary data."""

    classifiers: Classifiers = Classifiers()
    licenses: Licenses = Licenses()
    output: OutputCreator = OutputCreator()

    _files_list: list = list()

    def __attrs_post_init__(self) -> None:
        """Open JSON file of license aliases."""
        with open("data/license_dictionary.json") as f:
            self.license_dictionary = json.load(f).get("data")

    def create_file(self) -> None:
        """
        Pass all input files and create output, witch will be printed on STDOUT.

        :return: None
        """
        global COUNTER_DEBUG
        # comparator = Comparator(self.licenses.licenses_list, self.classifiers.classifiers_list)
        comparator = Comparator()
        for file_path in self._files_list[:]:
            # pass all listed metadata
            try:
                with open(file_path) as f:
                    json_solver = JsonSolver(json.load(f), f)
            except Exception as e:
                print("Broken or can't find file: ", file_path, f"error: {e}", file=sys.stderr)
                exit(1)

            package = Package()
            self.get_classifier_and_license(json_solver, package)
            if package.name and package.version and (package.license_version or package.classifier):
                if comparator.cmp(package):
                    # no warning
                    self.output.add_package(package)
                else:
                    # warning
                    self.output.add_package(package, warning=True)
                    pass

        print(COUNTER_DEBUG)
        self.output.print()

    def get_classifier_and_license(self, json_file: JsonSolver, package: Package) -> None:
        """
        Get classifier and license groups.

        :param json_file: json class witch hold data from file
        :param package: class package witch will hold all package data
        :return: None
        """
        package.set_file_path(json_file.path)

        package.set_package_name(json_file.get_package_name())
        package.set_version(json_file.get_package_version())

        classifier_name = json_file.get_classifier_name()
        license_name = json_file.get_license_name()

        self._get_license_group(license_name, package)
        self._get_classifier_group(classifier_name, package)

        # DEBUG
        if package.license and package.classifier:
            global COUNTER_DEBUG
            COUNTER_DEBUG += 1
            # package.print()

    def _get_license_group(self, license_name: str, package: Package) -> None:
        """
        Search for a group of entered license name.

        :param license_name: name of license to find in class license_list
        :param package: package info
        :return: None
        """
        # undetected license
        if license_name is None:
            return

        # UNKNOWN license name
        if license_name.lower() == "unknown":
            package.set_license(list(["UNKNOWN"]))
            return

        # pass license list
        for lic_li in self.licenses.licenses_list:
            lic_li_lower = [x.lower() for x in lic_li]
            if (
                license_name.lower() in lic_li_lower
                or _delete_brackets(license_name).lower() in lic_li_lower
                or _delete_brackets_and_content(license_name).lower() in lic_li_lower
            ):
                package.set_license(lic_li, set_version=True)
                return

        # try to found license without version of license or license in dictionary
        for lic_li in self.licenses.licenses_list:
            license_name_no_version, _ = _detect_version_and_delete(lic_li[len(lic_li) - 1])

            if self.license_dictionary.get(license_name.lower()) in lic_li:
                # license found in license dictionary
                _license = self.license_dictionary.get(license_name.lower())
                _license_li = [x for x in self.licenses.licenses_list if _license in x][0]
                package.set_license(_license_li, set_version=True)
                return

            elif license_name_no_version == license_name:
                # license found without license version
                package.set_license(list([license_name]))
                package.set_license_version("UNDETECTED")
                return
        return

    def _get_classifier_group(self, classifier_name, package: Package) -> None:
        """
        Search for a group of entered classifier name.

        :param classifier_name: name of license to find in class classifier list
        :param package: package info
        :return: None
        """
        if classifier_name is None:
            return

        for cla_li in self.classifiers.classifiers_list:
            if list(set(cla_li) & set(classifier_name)):
                package.set_classifier(cla_li)

    def get_file(self, file: str) -> None:
        """
        Add file to file_list.

        :param file: path to file
        :return: None
        """
        if file.lower().endswith(".json"):
            self._files_list.append(file)
        else:
            print(f"[ERROR]: wrong format you can insert only .json file: {file}", file=sys.stderr)
            exit(1)

    def get_dir_files(self, directory) -> None:
        """
        Create list of all files in directory.

        :param directory: path to directory
        :return: None
        """
        for f in os.listdir(directory):
            full_path = os.path.join(directory, f)
            if full_path.lower().endswith(".json"):
                self._files_list.append(full_path)
            else:
                print(f"[ERROR]: wrong format you can insert only .json SKIPPED: {f}", file=sys.stderr)
                exit(1)
