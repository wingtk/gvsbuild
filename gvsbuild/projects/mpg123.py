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
class Mpg123(Tarball, CmakeProject):
    def __init__(self):
        Project.__init__(
            self,
            "mpg123",
            version="1.33.7",
            repository="https://www.mpg123.de",
            archive_url="https://www.mpg123.de/download/mpg123-{version}.tar.bz2",
            hash="31d0e35a4ca567ec9b5ebda6c3062bb4435d6d3eacd6ef0d95cadd7854dc03ee",
            dependencies=["cmake", "ninja"],
        )

    def build(self):
        # The CMake build lives in ports/cmake. Only the library is needed by
        # gst-plugins-good's mpg123 element: no programs, no libout123/libsyn123.
        CmakeProject.build(
            self,
            cmake_params=[
                "-DBUILD_SHARED_LIBS=ON",
                "-DBUILD_LIBOUT123=OFF",
            ],
            use_ninja=True,
            source_part="ports/cmake",
        )
        self.install(r".\COPYING share\doc\mpg123")
