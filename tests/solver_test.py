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

"""Tests related to class Solver."""

import os
import pytest
from thoth.license_solver.solver import Solver


class TestSolver:
    """Test solver."""

    solver: Solver = Solver()

    # test get_license_group function
    def test_get_license_group_unknown(self) -> None:
        """Test detecting license group for unknown."""
        assert self.solver._get_license_group(None) == (list(["UNDETECTED"]), False)
        assert self.solver._get_license_group("UNKNOWN") == (list(["UNKNOWN"]), False)
        assert self.solver._get_license_group("uNkNOWN") == (list(["UNKNOWN"]), False)

    def test_get_license_group_found_in_license_list(self) -> None:
        """Test detecting license group in license."""
        bsd = ['BSD 4-Clause "Original" or "Old" License', "BSD-4-Clause", "BSD 4 Clause"]
        assert self.solver._get_license_group(bsd[0]) == (bsd, True)
        assert self.solver._get_license_group(bsd[1]) == (bsd, True)
        assert self.solver._get_license_group(bsd[2]) == (bsd, True)

        bsd_with_random_lowercase = ['bsd 4-ClaUse "Original" or "Old" License', "BsD-4-ClaUse", "BsD 4 Clause"]
        assert self.solver._get_license_group(bsd_with_random_lowercase[0]) == (bsd, True)
        assert self.solver._get_license_group(bsd_with_random_lowercase[1]) == (bsd, True)
        assert self.solver._get_license_group(bsd_with_random_lowercase[2]) == (bsd, True)

        # find license without version
        assert self.solver._get_license_group("Apache") == (list(["Apache"]), True)

    def test_get_license_group_in_file(self) -> None:
        """Test detecting license group in dictionary."""
        apache = ["Apache License 1.0", "Apache-1.0", "Apache 1.0"]
        assert self.solver._get_license_group("apache-1") == (apache, True)
        assert self.solver._get_license_group("APACHE-1") == (apache, True)

    def test_get_license_group_not_fount(self) -> None:
        """Test detecting license group not found."""
        assert self.solver._get_license_group("89fdslkj94") == (list(["UNDETECTED"]), False)

    # test get_classifier_group function
    def test_get_classifier_group_none(self) -> None:
        """Test detecting classifier group which output None."""
        assert self.solver._get_classifier_group(None) is None

    def test_get_classifier_group_found_in_classifier_list(self) -> None:
        """Test detecting classifier group found in classifier list."""
        classifier_input = ["License :: Aladdin Free Public License (AFPL)"]
        classifier_output = [
            "License :: Aladdin Free Public License (AFPL)",
            "Aladdin Free Public License (AFPL)",
            "Aladdin Free Public License",
            "AFPL",
        ]
        assert self.solver._get_classifier_group(classifier_input) == classifier_output

        classifier_input_2 = ["AFPL"]
        assert self.solver._get_classifier_group(classifier_input_2) == classifier_output

        # tests with lowercase
        classifier_input_3 = ["aFpl"]
        assert self.solver._get_classifier_group(classifier_input_3) == classifier_output

    @pytest.fixture(autouse=True)
    def capsys(self, capsys):
        """Capsys for Pytest."""
        self.capsys = capsys

    def test_solver(self):
        """Test Solver."""
        file_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "test_files", "solver", "test_solver_files"
        )
        self.solver.solve_from_directory(file_path)
        self.solver.print_output()

        out, err = self.capsys.readouterr()

        assert str(out) == str(
            '{"moto": {"1.3.15.dev221": {"license": {"full_name": "Apache", '
            '"identifier_spdx": "UNDETECTED", "identifier": "UNDETECTED"}, '
            '"license_version": "UNDETECTED", "classifier": [["License :: OSI Approved :: '
            'Apache Software License", "Apache Software License"]], "warning": false}}, '
            '"itk-segmentation": {"4.13.2": {"license": {"full_name": "Apache", '
            '"identifier_spdx": "UNDETECTED", "identifier": "UNDETECTED"}, '
            '"license_version": "UNDETECTED", "classifier": [["License :: OSI Approved :: '
            'Apache Software License", "Apache Software License"]], "warning": false}}, '
            '"great-expectations": {"0.11.0b0": {"license": {"full_name": "Apache License '
            '2.0", "identifier_spdx": "Apache-2.0", "identifier": "Apache 2.0"}, '
            '"license_version": "2.0", "classifier": [["License :: OSI Approved :: Apache '
            'Software License", "Apache Software License"]], "warning": false}}, '
            '"SQLAlchemy": {"1.3.15": {"license": {"full_name": "Apache License 1.1", '
            '"identifier_spdx": "Apache-1.1", "identifier": "Apache 1.1"}, '
            '"license_version": "1.1", "classifier": [["License :: OSI Approved :: MIT '
            'License", "MIT License"]], "warning": true}, "9.10": {"license": '
            '{"full_name": "UNDETECTED", "identifier_spdx": "UNDETECTED", "identifier": '
            '"UNDETECTED"}, "license_version": "UNDETECTED", "classifier": [["License :: '
            'OSI Approved :: MIT License", "MIT License"]], "warning": true}, "9.9": '
            '{"license": {"full_name": "Apache License 2.0", "identifier_spdx": '
            '"Apache-2.0", "identifier": "Apache 2.0"}, "license_version": "2.0", '
            '"classifier": [["License :: OSI Approved :: MIT License", "MIT License"]], '
            '"warning": true}}, "polyaxon-client": {"0.6.0": {"license": {"full_name": '
            '"MIT License", "identifier_spdx": "MIT", "identifier": "MIT"}, '
            '"license_version": "LICENSE-WITHOUT-VERSION", "classifier": '
            '[["UNDETECTED"]], "warning": false}}, "setuptools-scm": {"1.15.4": '
            '{"license": {"full_name": "MIT License", "identifier_spdx": "MIT", '
            '"identifier": "MIT"}, "license_version": "LICENSE-WITHOUT-VERSION", '
            '"classifier": [["License :: OSI Approved :: MIT License", "MIT License"]], '
            '"warning": false}}, "path.py": {"2.6.1": {"license": {"full_name": "MIT '
            'License", "identifier_spdx": "MIT", "identifier": "MIT"}, "license_version": '
            '"LICENSE-WITHOUT-VERSION", "classifier": [["License :: OSI Approved :: MIT '
            'License", "MIT License"]], "warning": false}}, "cwltool": '
            '{"1.0.20160108200940": {"license": {"full_name": "Apache License 2.0", '
            '"identifier_spdx": "Apache-2.0", "identifier": "Apache 2.0"}, '
            '"license_version": "2.0", "classifier": [["UNDETECTED"]], "warning": '
            'false}}, "django-redis-cache": {"1.5.1": {"license": {"full_name": '
            '"UNKNOWN", "identifier_spdx": "UNDETECTED", "identifier": "UNDETECTED"}, '
            '"license_version": "UNDETECTED", "classifier": [["UNDETECTED"]], "warning": '
            'false}}, "oslotest": {"4.2.0": {"license": {"full_name": "UNKNOWN", '
            '"identifier_spdx": "UNDETECTED", "identifier": "UNDETECTED"}, '
            '"license_version": "UNDETECTED", "classifier": [["License :: OSI Approved :: '
            'Apache Software License", "Apache Software License"]], "warning": false}}, '
            '"django-webpack-loader": {"0.0.6.1": {"license": {"full_name": "UNKNOWN", '
            '"identifier_spdx": "UNDETECTED", "identifier": "UNDETECTED"}, '
            '"license_version": "UNDETECTED", "classifier": [["License :: OSI Approved :: '
            'MIT License", "MIT License"]], "warning": false}}, "trimesh": {"2.29.9": '
            '{"license": {"full_name": "MIT License", "identifier_spdx": "MIT", '
            '"identifier": "MIT"}, "license_version": "LICENSE-WITHOUT-VERSION", '
            '"classifier": [["License :: OSI Approved :: MIT License", "MIT License"]], '
            '"warning": false}}}\n'
        )
