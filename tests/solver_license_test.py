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


"""Tests related to class SolverLicense."""

from thoth.license_solver.solver_license import SolverLicense


class TestSolverLicense:
    """Test SolverLicense."""

    def test_get_mit_license(self):
        """Test get."""
        solver = SolverLicense(
            {
                "test_1": {
                    "1.0": {
                        "license": ["MIT License", "MIT"],
                        "license_version": "LICENSE-WITHOUT-VERSION",
                        "classifier": [["fake classifier"]],
                        "warning": False,
                    }
                }
            }
        )

        # test license
        assert solver.get_license_full_name("test_1", "1.0") == "MIT License"
        assert solver.get_license_full_name("test_1", "bad_version") == "UNDETECTED"
        # test license identifier
        assert solver.get_license_idetentifier("test_1", "1.0") == "MIT"
        assert solver.get_license_idetentifier("test_1", "bad_version") == "UNDETECTED"
        # test license version
        assert solver.get_license_version("test_1", "1.0") == "LICENSE-WITHOUT-VERSION"
        assert solver.get_license_version("bad_name", "bad_version") == "UNDETECTED"
        # test warning
        assert solver.get_warning("test_1", "1.0") is False
        assert solver.get_warning("bad_name", "1.0") is True

        # test all
        assert solver.get_all("test_1", "1.0") == {
            "license": "MIT License",
            "license_identifier": "MIT",
            "license_version": "LICENSE-WITHOUT-VERSION",
            "warning": False,
        }

        assert solver.get_all("test_1", "bad_version") == {
            "license": "UNDETECTED",
            "license_identifier": "UNDETECTED",
            "license_version": "UNDETECTED",
            "warning": True,
        }
