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
from typing import List, Dict, Any
from .exceptions import UnableOpenFileData

_LOGGER = logging.getLogger(__name__)


@attr.s(slots=True)
class Licenses:
    """Class detect all licenses from downloaded data."""

    data = attr.ib(init=False, type=str)
    json_data = attr.ib(init=True, type=Dict[str, Any], default=dict())
    licenses: List[Any] = list()
    licenses_list: List[Any] = list()

    def __attrs_post_init__(self) -> None:
        """Run methods."""
        self.load_data()

    def load_data(self, file_path: str = "data/spdx_licenses.json") -> None:
        """Load data for classes variables."""
        file = os.path.join(os.path.dirname(os.path.realpath(__file__)), file_path)
        try:
            with open(file) as f:
                data = f.read()
                self.data = data
                self.json_data = json.loads(self.data)
                _LOGGER.debug("File spdx_licenses.json was successful loaded")
        except Exception:
            _LOGGER.critical("Could not open/read file: %s", file_path)
            raise UnableOpenFileData

        self._extract()

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
                else:
                    li.append(i["licenseId"])

                self.licenses_list.append(li)
        except Exception as e:
            _LOGGER.warning("Something bad with Indexing: %s", e)
