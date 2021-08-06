# author:   Viliam Podhajecky
# contact:  vpodhaje@redhat.com


import json
import sys
from license_solver.package import Package


class OutputCreator:
    """
    Propose of this class is to create dictionary for all packages (input)
    """
    file: dict = {}

    def add_package(self, package: Package, warning: bool = False) -> None:
        """
        Method add package to dictionary

        :param package: Package data
        :param warning: default False, if true create warning in package info
        :return: None
        """
        package_data = {
            "license": package.license,
            "license_version": str(package.license_version),
            "classifier": package.classifier,
        }

        if warning:
            package_data["warning"] = str(True)
        else:
            package_data["warning"] = str(False)

        if self.file.get(package.name) is None:
            self.file[package.name] = {
                package.version: package_data
            }
        else:
            if self.file[package.name].get(package.version) is None:
                self.file[package.name][package.version] = package_data
            else:
                self._check_duplicity(self.file[package.name].get(package.version), package_data)

    def _check_duplicity(self, old: dict, new: dict) -> None:
        """
        Method check version duplicity, if they don't match create warning in dict

        :param old: package in class dictionary
        :param new: new package witch want to be added
        :return: None
        """
        if old == new or old["warning"]:
            return
        else:
            for index in old:
                if old[index] is None and old[index] != new[index]:
                    old[index] = new[index]

                    if index == "license":
                        old["license_version"] = new["license_version"]

                elif old[index] != new[index]:
                    old["warning"] = True

    def print(self, indent=4):
        print(json.dumps(self.file, indent=indent), file=sys.stdout)
