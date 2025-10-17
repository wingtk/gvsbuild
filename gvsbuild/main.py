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

import rich
from cyclopts import App

import gvsbuild.groups  # noqa: F401
import gvsbuild.projects  # noqa: F401
import gvsbuild.tools  # noqa: F401
from gvsbuild.build import build
from gvsbuild.deps import deps
from gvsbuild.list import list_
from gvsbuild.outdated import outdated

rich.reconfigure(markup=False)

app = App(
    help="Build GTK for Windows",
    help_on_error=True,
)
app.command(build)
app.command(outdated)
app.command(name="list")(list_)
app.command(deps)

app.register_install_completion_command()


def run():
    app()
