#  Copyright (C) 2016 The Gvsbuild Authors
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, see <http://www.gnu.org/licenses/>.


"""Main build script."""

# Verify we can import from the script directory
import rich
import typer

from gvsbuild.deps import deps
from gvsbuild.list import list_

try:
    import gvsbuild.utils.utils  # noqa: F401
except ImportError:
    # We are probably using an embedded installation
    print("Error importing utility, fixing paths ...")
    import os
    import sys

    # Get the script dir
    script_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
    # and add it at the beginning, emulating the standard python startup
    sys.path.insert(0, script_dir)

import gvsbuild.groups  # noqa: F401
import gvsbuild.projects  # noqa: F401
import gvsbuild.tools  # noqa: F401
from gvsbuild.build import build
from gvsbuild.info import version_callback
from gvsbuild.outdated import outdated

rich.reconfigure(markup=False)

app = typer.Typer(help="Build GTK for Windows")
app.command(help="")(build)
app.command(help="")(outdated)
app.command(help="", name="list")(list_)
app.command(help="")(deps)


@app.callback()
def common(
    ctx: typer.Context,
    version: bool = typer.Option(
        None, "--version", callback=version_callback, help="Show the app's version"
    ),
):
    pass


def run():
    app()
