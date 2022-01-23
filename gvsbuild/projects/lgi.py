#  Copyright (C) 2016 - Yevgen Muntyan
#  Copyright (C) 2016 - Ignacio Casal Quinteiro
#  Copyright (C) 2016 - Arnavion
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

from gvsbuild.utils.base_expanders import GitRepo
from gvsbuild.utils.base_project import Project, project_add


@project_add
class Lgi(GitRepo, Project):
    def __init__(self):
        GitRepo.__init__(self)
        Project.__init__(
            self,
            "lgi",
            repo_url="https://github.com/pavouk/lgi.git",
            fetch_submodules=False,
            tag="2dd5db9678913ba08e54931b59cd97e550c7459e",
            dependencies=["luajit", "gobject-introspection"],
            patches=["fix-loading-non-libtool-style-libs.patch"],
        )

    def build(self):
        self.push_location("lgi")

        self.exec_vs(
            r'nmake -f .\Makefile-msvc.mak corelgilua51.dll version.lua PREFIX="%(gtk_dir)s'
        )

        self.install(r"corelgilua51.dll lib\lua\lgi")
        self.install(r".\*.lua share\lua\lgi")
        self.install(r".\override\*.lua share\lua\lgi\override")

        self.pop_location()

        self.install(r"LICENSE share\doc\lgi")
        self.install(r"lgi.lua share\lua")
