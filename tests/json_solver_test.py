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

"""Tests related to class JsonSolver."""

import json
import pytest
import os
from thoth.license_solver.json_solver import JsonSolver


class TestJsonSolver:
    """Test JsonSolver."""

    json_solver: JsonSolver
    json_solver_empty: JsonSolver

    @pytest.fixture(autouse=True)
    def _setup_json_solver_variables(self):
        """Set up class variables."""
        file_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "test_files", "json_solver", "load_json_file.json"
        )
        with open(file_path) as f:
            file_data = json.load(f)
        self.json_solver = JsonSolver(file_data, file_path)

        # create json_solver for empty file
        file_path_empty = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_files/json_solver/empty.json")
        with open(file_path_empty) as f:
            file_data_empty = json.load(f)

        self.json_solver_empty = JsonSolver(file_data_empty, file_path_empty)

    def test_get_package_name(self):
        """Test get_package_name."""
        assert self.json_solver.get_package_name() == "setuptools-scm"
        assert self.json_solver_empty.get_package_name() is None

    def test_get_package_version(self):
        """Test get_package_version."""
        assert self.json_solver.get_package_version() == "1.15.4"
        assert self.json_solver_empty.get_package_version() is None

    def test_get_license_name(self):
        """Test get_license_name."""
        assert self.json_solver.get_license_name() == "MIT"
        assert self.json_solver_empty.get_license_name() is None

    def test_get_classifier_name(self):
        """Test get_classifier_name."""
        classifier = [
            "Development Status :: 4 - Beta",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 2.6",
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3.3",
            "Programming Language :: Python :: 3.4",
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: 3.6",
            "Topic :: Software Development :: Libraries",
            "Topic :: Software Development :: Version Control",
            "Topic :: System :: Software Distribution",
            "Topic :: Utilities",
        ]
        assert self.json_solver.get_classifier_name() == classifier
        assert self.json_solver_empty.get_classifier_name() is None
