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
class Libcbor(Tarball, CmakeProject):
    def __init__(self):
        Project.__init__(
            self,
            "libcbor",
            version="0.13.0",
            repository="https://github.com/PJK/libcbor",
            archive_url="https://github.com/PJK/libcbor/archive/refs/tags/v{version}.tar.gz",
            archive_filename="libcbor-{version}.tar.gz",
            hash="95a7f0dd333fd1dce3e4f92691ca8be38227b27887599b21cd3c4f6d6a7abb10",
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
