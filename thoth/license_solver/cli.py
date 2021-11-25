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
# type: ignore[misc]

"""solver-license-jon CLI."""
import os
import sys

import click
import logging
from thoth.common import init_logging
from thoth.license_solver.solver import Solver

init_logging()
_LOGGER = logging.getLogger("thoth.license_solver")


@click.command()
@click.pass_context
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    envvar="THOTH_SOLVER_LICENSE_JOB_DEBUG",
    help="Be verbose about what's going on.",
)
@click.option(
    "-f",
    "--file",
    nargs=1,
    type=str,
    help="Get license from file",
    envvar="THOTH_SOLVER_LICENSE_JOB_FILE",
)
@click.option(
    "-d",
    "--directory",
    nargs=1,
    type=str,
    help="Get licenses from folder",
    envvar="THOTH_SOLVER_LICENSE_JOB_DIRECTORY",
)
@click.option(
    "-pv",
    "--package-version",
    nargs=1,
    type=str,
    help="Package version",
    envvar="THOTH_SOLVER_LICENSE_PACKAGE_VERSION",
)
@click.option(
    "-pn",
    "--package-name",
    nargs=1,
    type=str,
    help="Package name detect from PyPI",
    envvar="THOTH_SOLVER_LICENSE_PACKAGE_NAME",
)
def cli(
    _: click.Context,
    directory: str,
    file: str,
    package_name: str,
    package_version: str,
    verbose: bool = False,
) -> None:
    """
    License solver.

    License-solver handles license detection and classifier detection from metadata provided by PyPI.
    The program prints the result in the form of JSON on STDOUT.
    """
    if verbose:
        _LOGGER.setLevel(logging.DEBUG)
        _LOGGER.debug("Debug mode is on")

    license_solver = Solver()

    if package_name or package_version:
        if package_name and package_version:
            _LOGGER.debug("Parsing PyPI: {} {}", package_name, package_version)
            license_solver.solve_from_pypi(package_name, package_version)
            license_solver.print_output()
        else:
            _LOGGER.error("Must be parsed package_name and package_version at same time.")
            print("Must be parsed package_name and package_version at same time.", file=sys.stderr)
            exit(1)

    if directory and file:
        _LOGGER.error("Can't be directory and file parsed at same time.")
        print("Can't be directory and file parsed at same time. Choose only one", file=sys.stderr)
        exit(1)
    elif directory:
        if not os.path.isdir(directory):
            _LOGGER.warning("You need to insert valid directory.")
            return

        _LOGGER.debug("Parsing directory: %s", directory)
        license_solver.solve_from_directory(directory)
        license_solver.print_output()
    elif file:
        _LOGGER.debug("Parsing file: %s", file)
        license_solver.solve_from_file(file)
        license_solver.print_output()


__name__ == "__main__" and cli()
