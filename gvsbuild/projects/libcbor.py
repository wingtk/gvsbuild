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

from gvsbuild.utils.base_builders import CmakeProject
from gvsbuild.utils.base_expanders import Tarball
from gvsbuild.utils.base_project import Project, project_add


@project_add
class Libcbor(Tarball, CmakeProject):
    def __init__(self):
        Project.__init__(
            self,
            "libcbor",
            version="0.10.2",
            archive_url="https://github.com/PJK/libcbor/archive/refs/tags/v{version}.tar.gz",
            hash="e75f712215d7b7e5c89ef322a09b701f7159f028b8b48978865725f00f79875b",
            archive_filename="libcbor-{version}.tar.gz",
            dependencies=["cmake", "ninja"],
        )

    def build(self):
        # If do_install is True, the build fails
        CmakeProject.build(self, use_ninja=True, do_install=False)
        self.install(r"_gvsbuild-cmake\src\cbor.lib lib")
        self.install(r"_gvsbuild-cmake\src\cbor\*.h include\cbor")
        self.install(r"_gvsbuild-cmake\cbor\*.h include\cbor")
        self.install(r"src\cbor.h include")
        self.install(r"src\cbor\*.h include\cbor")
