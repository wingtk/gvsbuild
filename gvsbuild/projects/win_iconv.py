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
class WinIconv(Tarball, CmakeProject):
    def __init__(self):
        Project.__init__(
            self,
            "win-iconv",
            version="0.0.10",
            archive_url="https://github.com/win-iconv/win-iconv/archive/v{version}.tar.gz",
            archive_filename="win-iconv-{version}.tar.gz",
            hash="58493387c7c9c70d61e711ec2feec5db0a59d164556642d2b427dde4ef756bc1",
            dependencies=[
                "cmake",
                "ninja",
            ],
            patches=[
                "0001-CMakeLists.txt-Remove-debug-postfix.patch",
            ],
        )

    def build(self):
        CmakeProject.build(self, use_ninja=True, cmake_params="-DBUILD_TEST=1")

        self.install(r".\COPYING share\doc\win-iconv")
