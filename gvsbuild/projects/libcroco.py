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

from gvsbuild.utils.base_expanders import Tarball
from gvsbuild.utils.base_project import Project, project_add


@project_add
class Libcroco(Tarball, Project):
    def __init__(self):
        Project.__init__(
            self,
            "libcroco",
            version="0.6.13",
            lastversion_even=True,
            repository="https://gitlab.gnome.org/Archive/libcroco",
            archive_url="https://download.gnome.org/sources/libcroco/{major}.{minor}/libcroco-{version}.tar.xz",
            hash="767ec234ae7aa684695b3a735548224888132e063f92db585759b422570621d4",
            dependencies=["glib", "libxml2"],
        )

    def build(self):
        self.exec_msbuild_gen(r"win32", "libcroco.sln")
        self.install(r".\COPYING share\doc\libcroco")
