# author:   Viliam Podhajecky
# contact:  vpodhaje@redhat.com

import sys
import urllib.request
import json
import attr
from typing import Dict, Any, List, Optional


@attr.s
class Licenses:
    _received_text: str = ""
    json_data: dict = dict()
    licenses: list = list()
    licenses_list: list = list()

    def __attrs_post_init__(self) -> None:
        self._download_licenses()
        self._cmp_sets_of_data()
        self._extract()

    def _download_licenses(self) -> None:
        """
            Download licenses from SPDX and load
            link to repo: https://github.com/spdx/license-list-data
        """
        url_json = "https://raw.githubusercontent.com/spdx/license-list-data/master/json/licenses.json"
        try:
            response = urllib.request.urlopen(url_json)
            data = response.read()
            self._received_text = data.decode('utf-8')
            self.json_data = json.loads(self._received_text)
        except ValueError as e:
            print(f"Can't load file.\n Error: {e}", file=sys.stderr)
        except Exception as e:
            # no internet connection or url to download data are wrong
            # in next step will load local file
            print("[Error] in downloading licenses from SPDX:", e, file=sys.stderr)
            pass

    def _cmp_sets_of_data(self) -> None:
        local_path = "data/spdx_licenses.json"

        with open(local_path) as f:
            data = json.load(f)

        if not self._received_text:
            print("[Error] in downloading files from server or broken document. Using local file.", file=sys.stderr)
            self._received_text = data
            self.json_data = data

    def _extract(self) -> None:
        try:
            for i in self.json_data["licenses"]:
                # original data
                self.licenses.append(i)
                # list of data
                li = list()
                li.append(i["name"])
                li.append(i["licenseId"])

                if i["licenseId"] != i["licenseId"].replace("-", " "):
                    # abbreviation without "-"
                    li.append(i["licenseId"].replace("-", " "))

                self.licenses_list.append(li)
            # print(*self.licenses_list, sep="\n")
        except IndexError as e:
            print(f"Something bad with Indexing: {e}", file=sys.stderr)
        except Exception as e:
            print(f"Exception. Nice to know but WTF?: {e}", file=sys.stderr)
