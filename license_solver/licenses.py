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

"""Class download licenses and extract data from them."""

import sys
import urllib.request
import json
import attr


@attr.s
class Licenses:
    """Class detect all licenses from downloaded data."""

    _received_text: str = ""
    json_data: dict = dict()
    licenses: list = list()
    licenses_list: list = list()

    def __attrs_post_init__(self) -> None:
        """Run methods."""
        self._download_licenses()
        self._cmp_sets_of_data()
        self._extract()

    def _download_licenses(self) -> None:
        """
        Download licenses from SPDX and load.

        link to repo: https://github.com/spdx/license-list-data
        """
        url_json = "https://raw.githubusercontent.com/spdx/license-list-data/master/json/licenses.json"
        try:
            response = urllib.request.urlopen(url_json)
            data = response.read()
            self._received_text = data.decode("utf-8")
            self.json_data = json.loads(self._received_text)
        except ValueError as e:
            print(f"Can't load file.\n Error: {e}", file=sys.stderr)
        except Exception as e:
            # no internet connection or url to download data are wrong
            # in next step will load local file
            print("[Error] in downloading licenses from SPDX:", e, file=sys.stderr)
            pass

    def _cmp_sets_of_data(self) -> None:
        """Compare sets od data."""
        local_path = "data/spdx_licenses.json"

        with open(local_path) as f:
            data = json.load(f)

        if not self._received_text:
            print("[Error] in downloading files from server or broken document. Using local file.", file=sys.stderr)
            self._received_text = data
            self.json_data = data

    def _extract(self) -> None:
        """Extract licenses from downloaded data."""
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
