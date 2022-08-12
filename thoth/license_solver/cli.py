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
from thoth.license_solver import __version__ as license_solver_version

init_logging()
_LOGGER = logging.getLogger("thoth.license_solver")


def _print_version(ctx: click.Context, _, value: str) -> None:
    """Print license-solver version and exit."""
    if not value or ctx.resilient_parsing:
        return

    click.echo(license_solver_version)
    ctx.exit()


class OptionEatAll(click.Option):
    """
    Eat all argument of parameter.

    source: https://stackoverflow.com/a/48394004
    """

    def __init__(self, *args, **kwargs):
        """Initialize."""
        self.save_other_options = kwargs.pop("save_other_options", True)
        nargs = kwargs.pop("nargs", -1)
        assert nargs == -1, "nargs, if set, must be -1 not {}".format(nargs)
        super(OptionEatAll, self).__init__(*args, **kwargs)
        self._previous_parser_process = None
        self._eat_all_parser = None

    def add_to_parser(self, parser, ctx):
        """Add to parser."""

        def parser_process(value, state):
            """Parser process."""
            # method to hook to the parser.process
            done = False
            value = [value]
            if self.save_other_options:
                # grab everything up to the next option
                while state.rargs and not done:
                    for prefix in self._eat_all_parser.prefixes:
                        if state.rargs[0].startswith(prefix):
                            done = True
                    if not done:
                        value.append(state.rargs.pop(0))
            else:
                # grab everything remaining
                value += state.rargs
                state.rargs[:] = []
            value = tuple(value)

            # call the actual process
            self._previous_parser_process(value, state)

        retval = super(OptionEatAll, self).add_to_parser(parser, ctx)
        for name in self.opts:
            our_parser = parser._long_opt.get(name) or parser._short_opt.get(name)
            if our_parser:
                self._eat_all_parser = our_parser
                self._previous_parser_process = our_parser.process
                our_parser.process = parser_process
                break
        return retval


@click.command(context_settings=dict(max_content_width=160))
@click.pass_context
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    help="Be verbose about what's going on.",
    envvar="THOTH_SOLVER_LICENSE_JOB_DEBUG",
)
@click.option(
    "--version",
    is_flag=True,
    is_eager=True,
    callback=_print_version,
    expose_value=False,
    help="Print license-solver version and exit.",
)
@click.option(
    "-f",
    "--file",
    type=tuple,
    cls=OptionEatAll,
    help="Get license from file.",
    envvar="THOTH_SOLVER_LICENSE_JOB_FILE",
)
@click.option(
    "-d",
    "--directory",
    type=tuple,
    cls=OptionEatAll,
    help="Get licenses from folder.",
    envvar="THOTH_SOLVER_LICENSE_JOB_DIRECTORY",
)
@click.option(
    "-pn",
    "--package-name",
    type=tuple,
    cls=OptionEatAll,
    help='Get license from latest PyPI release or use with "--package-version" for specific version.',
    envvar="THOTH_SOLVER_LICENSE_PACKAGE_NAME",
)
@click.option(
    "-pv",
    "--package-version",
    nargs=1,
    type=str,
    help="Get license with specific version.",
    envvar="THOTH_SOLVER_LICENSE_PACKAGE_VERSION",
)
@click.option(
    "-o",
    "--output",
    type=str,
    help="Save output to JSON file.",
    envvar="THOTH_SOLVER_LICENSE_OUTPUT",
)
@click.option(
    "-np",
    "--no-print",
    is_flag=True,
    help="No print on STDOUT.",
    envvar="THOTH_SOLVER_LICENSE_NO_PRINT",
)
@click.option(
    "-pp",
    "--pretty-printing",
    type=int,
    nargs=1,
    default=-1,
    show_default=True,
    help="Save/print result with prettier look.",
    envvar="THOTH_SOLVER_LICENSE_INDENT",
)
@click.option(
    "-gch",
    "--github-check",
    is_flag=True,
    help="Check licenses with Github repository.",
    envvar="THOTH_SOLVER_LICENSE_GITHUB_CHECK",
)
def cli(
    ctx: click.Context,
    directory: tuple,
    file: tuple,
    package_name: str,
    package_version: str,
    output: str,
    no_print: bool,
    pretty_printing: int,
    github_check: bool = False,
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

    license_solver = Solver(github_check)

    # package argument
    if package_name is not None:
        if len(package_name) > 1:
            if package_version:
                _LOGGER.warning("Can't insert version to multiple package_name entry.")
                exit(1)

            for pn in package_name:
                license_solver.solve_from_pypi(pn, package_version)

        elif len(package_name) == 1:
            license_solver.solve_from_pypi(package_name[0], package_version)
        elif package_version:
            print(ctx.get_help(), "\n\n--package-version is used with --package-name.", file=sys.stderr)
            exit(1)

    # directory argument
    if directory:
        for d in directory:
            if not os.path.isdir(d):
                _LOGGER.warning("Not a valid directory %r [SKIPPED].", d)
                continue

            _LOGGER.debug("Parsing directory: %s", d)
            license_solver.solve_from_directory(d)

    # file argument
    if file:
        for f in file:
            if not os.path.isfile(f):
                _LOGGER.warning("Not a valid file %r [SKIPPED].", f)
                continue

            _LOGGER.debug("Parsing file: %s", f)
            license_solver.solve_from_file(f)

    if output:
        license_solver.save_output(output, pretty_printing)

    if not no_print:
        license_solver.print_output(pretty_printing)


__name__ == "__main__" and cli()
