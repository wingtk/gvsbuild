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

import os

from gvsbuild.utils.base_builders import CmakeProject
from gvsbuild.utils.base_expanders import Tarball
from gvsbuild.utils.base_project import Project, project_add


@project_add
class Libfido2(Tarball, CmakeProject):
    def __init__(self):
        Project.__init__(
            self,
            "libfido2",
            version="1.15.0",
            archive_url="https://developers.yubico.com/libfido2/Releases/libfido2-{version}.tar.gz",
            hash="abaab1318d21d262ece416fb8a7132fa9374bda89f6fa52b86a98a2f5712b61e",
            dependencies=[
                "cmake",
                "ninja",
                "zlib",
                "openssl",
                "libcbor",
            ],
            patches=[
                "0001-libfido2-update-cmake-script-to-have-sdl-flag-before.patch",
            ],
        )

    def build(self):
        if self.builder.x86:
            arch = "x86"
        else:
            arch = "x64"

        include_dirs = os.path.join(self.builder.gtk_dir, "inc")
        lib_dirs = os.path.join(self.builder.gtk_dir, "lib")
        bin_dirs = lib_dirs = os.path.join(self.builder.gtk_dir, "bin")

        build_params = "-DBUILD_EXAMPLES=OFF -DBUILD_MANPAGES=OFF -DBUILD_TESTS=OFF -DBUILD_TOOLS=OFF -DBUILD_STATIC_LIBS=OFF"
        cmake_params = f"-DWITH_ZLIB=ON -DCBOR_INCLUDE_DIRS={include_dirs} -DCRYPTO_INCLUDE_DIRS={include_dirs} -DZLIB_INCLUDE_DIRS={include_dirs} -DCBOR_LIBRARY_DIRS={lib_dirs} -DCRYPTO_LIBRARY_DIRS={lib_dirs} -DZLIB_LIBRARY_DIRS={lib_dirs} -DCBOR_BIN_DIRS={bin_dirs} -DCRYPTO_BIN_DIRS={bin_dirs} -DZLIB_BIN_DIRS={bin_dirs} -DCRYPTO_LIBRARIES=libcrypto {build_params}"

        CmakeProject.build(self, cmake_params=cmake_params, use_ninja=True)
        self.install(r"output\%s\static\* ." % (arch))
