# author:   Viliam Podhajecky
# contact:  vpodhaje@redhat.com
import re
from typing import Union, Tuple

def _detect_version_and_delete(string: str) -> Union[Tuple[str, str], Tuple[str, None]]:
    """
    Delete version of license from string
    :returns tuple
        - license name without version - first output
        - version - second output
    """

    regex = r"( v\d+\.| \d| version |, version)(\.\d|\d)*[\w]*"

    try:
        find = re.search(regex, string)
        if find:
            return re.sub(regex, '', string).strip(), find.group(0).strip()
        else:
            return re.sub(regex, '', string).strip(), None
    except Exception:
        return re.sub(regex, '', string).strip(), None


class Package(object):
    """Object which store values metadata"""
    name: str
    version: str
    license: list
    license_version: str
    classifier: list = list()
    file_path: str

    def set_package_name(self, package_name):
        """Set package name"""
        self.name = package_name

    def set_version(self, version):
        """Set version of package name"""
        self.version = version

    def set_license(self, license_name: list, set_version: bool = False):
        """Set type of license"""
        if set_version:
            _license_name_no_version, _license_version = _detect_version_and_delete(license_name[len(license_name) - 1])
            if _license_version is None:
                self.set_license_version("UNDETECTED")
            else:
                self.set_license_version(_license_version)
            self.license = license_name
        else:
            self.license = license_name

    def set_license_version(self, license_version: str):
        """Set version of license"""
        self.license_version = license_version

    def set_classifier(self, classifier):
        """Set classifier"""
        if self.classifier is None:
            self.classifier = [classifier]
        else:
            self.classifier.append(classifier)

    def set_file_path(self, path):
        self.file_path = path

    def print(self):
        """Print class property on STDOUT"""
        print(
            f"package:\t\t {self.name}\n"
            f"version:\t\t {self.version}\n"
            f"license:\t\t {self.license}\n"
            f"license_version: {self.license_version}\n"
            f"classifier:\t\t {self.classifier}\n"
            f"file_path:\t\t {self.file_path}"
        )
