# author:   Viliam Podhajecky
# contact:  vpodhaje@redhat.com

import re
import sys
import yaml
from attr import attrs, attrib
from license_solver.classifiers import Classifiers
from license_solver.licenses import Licenses
from license_solver.package import _detect_version_and_delete, Package


def _delete_brackets(license_list: str):
    return re.sub(r"(\(?)(\)?)", '', license_list).strip()


def _delete_brackets_and_content(license_list: str):
    return re.sub(r"\(.*?\)", '', license_list).strip()


@attrs
class Comparator:
    """Class Comparator compare classifiers and licenses"""
    # licenses: Licenses.licenses_list = attrib()
    # classifiers: Classifiers.classifiers_list = attrib()
    counter: int = 0

    def __attrs_post_init__(self):
        # create copy licenses and classifier, because we don't want to edit original lice/class data
        # self.licenses = self.licenses.copy()
        # self.classifiers = self.classifiers.copy()

        # open file
        with open("data/comparator_dictionary.yaml", "r") as f:
            try:
                self._comparator_dictionary = yaml.safe_load(f)
            except yaml.YAMLError:
                print("Can't open data/comparator_dictionary.yaml", file=sys.stderr) and exit(1)

    def cmp(self, package: Package) -> bool:
        """
        Method compare License and Classifier from package data

        :param package: Package from input
        :return: True if match, False if not
        """
        _license = package.license
        _classifier = package.classifier

        if _license is None or _classifier is None:
            return True

        for x in _classifier:
            if list(set(_license) & set(x)) or self.search_in_dictionary(_license, x) or _license[0] == "UNKNOWN" or \
                    _license[0].lower() == "the unlicense":
                # print("Match ", list(set(_license) & set(_classifier[0])), "\n") # DEBUG
                return True

        # print("Warning\n")
        return False

    def search_in_dictionary(self, license, classifier) -> bool:
        """
        Method is searching for alias in data/comparator_dictionary.yaml

        :param license: License to compare with classifier
        :param classifier: Classifier to compare with license
        :return: True if found match, False if not
        """
        if self._comparator_dictionary["classifier"].get(classifier[1]) is not None:
            for x in self._comparator_dictionary["classifier"].get(classifier[1]):
                if x == license[0]:
                    # print(x) # DEBUG
                    return True

        return False
