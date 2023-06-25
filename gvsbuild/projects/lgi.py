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

from gvsbuild.utils.base_builders import Meson
from gvsbuild.utils.base_expanders import GitRepo
from gvsbuild.utils.base_project import Project, project_add


@project_add
class Lgi(GitRepo, Meson):
    def __init__(self):
        Project.__init__(
            self,
            "lgi",
            repo_url="https://github.com/pavouk/lgi.git",
            fetch_submodules=False,
            tag="4a12286ffd5ec162a50efeff3c4896d6cd14c43c",
            dependencies=["luajit", "gobject-introspection"],
        )
        self.add_param("-Dtests=false")
        self.add_param("-Dlua-bin=luajit")

    def build(self):
        Meson.build(self)
        self.install(r"LICENSE share\doc\lgi")
