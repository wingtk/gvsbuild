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

from gvsbuild.utils.base_builders import CmakeProject
from gvsbuild.utils.base_expanders import Tarball
from gvsbuild.utils.base_project import Project, project_add


@project_add
class Expat(Tarball, CmakeProject):
    def __init__(self):
        Project.__init__(
            self,
            "expat",
            version="2.6.3",
            repository="libexpat",
            archive_url="https://github.com/libexpat/libexpat/releases/download/R_{major}_{minor}_{micro}/expat-{version}.tar.xz",
            hash="274db254a6979bde5aad404763a704956940e465843f2a9bd9ed7af22e2c0efc",
            dependencies=["cmake", "ninja"],
            patches=["0001-CMakeLists-do-not-add-postfix-d-in-debug-builds.patch"],
        )

    def build(self):
        CmakeProject.build(self, use_ninja=True)
        self.install(r".\COPYING share\doc\expat")
