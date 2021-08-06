# author:   Viliam Podhajecky
# contact:  vpodhaje@redhat.com
import re
import sys
import urllib.request
from attr import attrs
from typing import Dict, Any, List, Optional
from license_solver.package import _detect_version_and_delete


def _get_abbreviation(classifier: str) -> list:
    """Abbreviation for license name"""

    abbreviation = list()
    start = classifier.find("(")
    end = classifier.find(")")
    if start != -1 and end != -1:
        txt = classifier[classifier.find("(") + 1:classifier.find(")")]
        abbreviation.append(txt)
    return abbreviation


def _get_name_license(classifier: str) -> str:
    """Get licence name from classifier string"""
    data = classifier.split("::")

    if len(data) > 0 and len(data[len(data) - 1]) > 1:
        return data[len(data) - 1].strip()[0:]
    else:
        return ""


@attrs
class Classifiers:
    _received_text: str = ""
    classifiers: list = list()
    classifiers_list: list = list()

    def __attrs_post_init__(self):
        """INIT method"""
        self._download_classifiers()
        self._cmp_sets_of_data()
        self._extract_classifiers()

    def _download_classifiers(self) -> None:
        """Download classifiers from PyPI"""
        url = "https://pypi.org/pypi?%3Aaction=list_classifiers"
        try:
            response = urllib.request.urlopen(url)
            data = response.read()
            self._received_text = data.decode('utf-8')
        except Exception as e:
            # no internet connection or url to download data are wrong
            print(f"[Error] in downloading classifiers from PyPI: {e}", file=sys.stderr)
            pass

    def _cmp_sets_of_data(self) -> None:
        """
            Before calling this function will be downloaded data from PyPI and after this compared with local file
            If file will be different, than will be used downloaded (after checking (broken, etc.) )
        """
        local_path = "data/pypi_classifiers.txt"
        with open(local_path, "r") as file:
            data = file.read()

        if not self._received_text or self._received_text.find("License ::") == -1:
            print("[Error] in downloading files from server or broken document. Using local file. ", file=sys.stderr)
            self._received_text = data

    def _convert_to_list(self) -> None:
        """Covert downloaded string to list"""
        self.classifiers = list(self._received_text.split("\n"))

    def _extract(self) -> None:
        """Extract licence from classifiers list"""
        for classifier_full in self.classifiers:
            if len(classifier_full) >= 7 and classifier_full.startswith("License"):
                # append licenses to list
                classifier_name = _get_name_license(classifier_full)
                classifier_abbreviation = _get_abbreviation(classifier_full)

                li = list()
                li.append(classifier_full)  # full classifier name
                li.append(classifier_name)  # only name without "License :: ..."

                # abbreviation
                if len(classifier_abbreviation) > 0:
                    for abbre in classifier_abbreviation:
                        classifier_no_abbreviation = classifier_name.replace(f"({abbre})", "").strip()
                        classifier_no_abbreviation = classifier_no_abbreviation.replace(f"  ", " ")
                        if classifier_name != classifier_no_abbreviation:
                            li.append(classifier_no_abbreviation)  # name without abbreviation

                        li.append(abbre)  # abbreviation
                        _x = abbre.replace("-", " ")
                        if _x != abbre:
                            li.append(_x)

                self.classifiers_list.append(li)

    def _extract_classifiers(self) -> None:
        """Extract classifiers from downloaded data"""
        self._convert_to_list()
        self._extract()
