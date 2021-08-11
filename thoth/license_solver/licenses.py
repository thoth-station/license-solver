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

"""Class download licenses and extract data from them."""

import os
import attr
import json
import logging
import requests
from typing import List, Dict, Any

_LOGGER = logging.getLogger(__name__)


@attr.s(slots=True)
class Licenses:
    """Class detect all licenses from downloaded data."""

    received_text = attr.ib(init=False, type=str)
    json_data = attr.ib(init=True, type=Dict[str, Any], default=dict())
    licenses: List[Any] = list()
    licenses_list: List[Any] = list()

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
        response = requests.get(url_json)

        if response.status_code != 200:
            print("[Error] in downloading licenses from SPDX")
        else:
            self.received_text = response.text
            self.json_data = json.loads(self.received_text)

    def _cmp_sets_of_data(self) -> None:
        """Compare sets od data."""
        if not hasattr(self, "received_text") or not self.received_text:
            file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data/spdx_licenses.json")
            with open(file_path) as f:
                data = json.load(f)

            self.received_text = data
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
            _LOGGER.warning(f"Something bad with Indexing: {e}")
        except Exception as e:
            _LOGGER.warning(f"Exception. Nice to know but WTF?: {e}")
