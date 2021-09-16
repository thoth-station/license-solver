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
def cli(_: click.Context, directory: str, file: str, verbose: bool = False) -> None:
    """
    License solver.

    License-solver handles license detection and classifier detection from metadata provided by PyPI.
    The program prints the result in the form of JSON on STDOUT.
    """
    if verbose:
        _LOGGER.setLevel(logging.DEBUG)
        _LOGGER.debug("Debug mode is on")

    license_solver = Solver()

    if directory and file:
        _LOGGER.error("Can't be directory and file parsed at same time.")
        exit(1)

    if directory:
        _LOGGER.debug("Parsing directory: %s", file)
        license_solver.solve_from_directory(directory)
        license_solver.print_output()

    if file:
        _LOGGER.debug("Parsing file: %s", file)
        license_solver.solve_from_file(file)
        license_solver.print_output()


__name__ == "__main__" and cli()
