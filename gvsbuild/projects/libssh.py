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
class Libssh(Tarball, CmakeProject):
    def __init__(self):
        Project.__init__(
            self,
            "libssh",
            archive_url="https://www.libssh.org/files/0.9/libssh-0.9.3.tar.xz",
            hash="2c8b5f894dced58b3d629f16f3afa6562c20b4bdc894639163cf657833688f0c",
            dependencies=["zlib", "openssl", "cmake", "ninja"],
        )

    def build(self):
        CmakeProject.build(self, cmake_params="-DWITH_ZLIB=ON", use_ninja=True)
        self.install(r".\COPYING share\doc\libssh")


@project_add
class Libssh2(Tarball, CmakeProject):
    def __init__(self):
        Project.__init__(
            self,
            "libssh2",
            archive_url="https://www.libssh2.org/download/libssh2-1.8.0.tar.gz",
            hash="39f34e2f6835f4b992cafe8625073a88e5a28ba78f83e8099610a7b3af4676d4",
            dependencies=[
                "cmake",
                "ninja",
            ],
        )

    def build(self):
        CmakeProject.build(self, cmake_params="-DWITH_ZLIB=ON", use_ninja=True)
        self.install(r".\COPYING share\doc\libssh2")
