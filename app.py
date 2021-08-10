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
# type: ignore

"""solver-license-jon CLI."""

from license_solver import LicenseSolver
import click


@click.command()
@click.pass_context
@click.option(
    "-f",
    "--file",
    nargs=1,
    type=str,
    help="Get license from file",
)
@click.option(
    "-d",
    "--directory",
    nargs=1,
    type=str,
    help="Get licenses from folder",
)
# type ignore [misc]
def cli(
    _: click.Context,
    directory: str,
    file: str,
) -> None:
    """Parse program arguments."""
    license_solver = LicenseSolver()

    if directory:
        print("DIRECTORY")
        license_solver.get_dir_files(directory)

    if file:
        print("FILE")
        license_solver.get_file(file)

    license_solver.create_file()


__name__ == "__main__" and cli()
