# author:   Viliam Podhajecky
# contact:  vpodhaje@redhat.com

from attr import attrs, attrib


@attrs
class JsonSolver(object):
    """Class JsonSolver extend class LicenseSolver, help inquiry json data from metadata"""
    json_file: dict = attrib()
    path: object = attrib()

    def get_package_name(self):
        """Get package name from metadata"""
        try:
            return self.json_file["result"]["tree"][0].get("package_name")
        except Exception:
            return None

    def get_package_version(self):
        """Get package version from metadata"""
        try:
            return self.json_file["result"]["tree"][0].get("package_version")
        except Exception:
            return None

    def get_license_name(self):
        """Get license name from metadata"""
        try:
            return self.json_file["result"]["tree"][0]["importlib_metadata"]["metadata"].get("License")
        except Exception:
            return None

    def get_classifier_name(self):
        """Get classifier name from metadata"""
        try:
            return self.json_file["result"]["tree"][0]["importlib_metadata"]["metadata"].get("Classifier")
        except Exception:
            return None

    def get_errors(self):
        """Check if errors occurred:
            - result->errors
            - result->unparsed
            - result->unresolved
        """
        try:
            return not (self.json_file["result"].get("errors") or self.json_file["result"].get("unparsed") or
                        self.json_file["result"].get("unresolved"))
        except Exception as e:
            return False
