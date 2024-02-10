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
class Libuv(Tarball, CmakeProject):
    def __init__(self):
        Project.__init__(
            self,
            "libuv",
            version="1.48.0",
            archive_filename="libuv-v{version}.tar.gz",
            archive_url="https://github.com/libuv/libuv/archive/v{version}.tar.gz",
            hash="8c253adb0f800926a6cbd1c6576abae0bc8eb86a4f891049b72f9e5b7dc58f33",
            dependencies=[
                "cmake",
                "ninja",
            ],
        )

    def build(self):
        CmakeProject.build(self, use_ninja=True)

        self.install(r".\LICENSE share\doc\libuv")
