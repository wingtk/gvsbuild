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
            version="1.17.0",
            repository="https://github.com/yubico/libfido2",
            archive_url="https://developers.yubico.com/libfido2/Releases/libfido2-{version}.tar.gz",
            hash="c1012c8871d71b65872fd5ff1a9d6b0838a55683a03e85ba97479ce57129c736",
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

        cmake_params = [
            "-DWITH_ZLIB=ON",
            f"-DCBOR_INCLUDE_DIRS={include_dirs}",
            f"-DCRYPTO_INCLUDE_DIRS={include_dirs}",
            f"-DZLIB_INCLUDE_DIRS={include_dirs}",
            f"-DCBOR_LIBRARY_DIRS={lib_dirs}",
            f"-DCRYPTO_LIBRARY_DIRS={lib_dirs}",
            f"-DZLIB_LIBRARY_DIRS={lib_dirs}",
            f"-DCBOR_BIN_DIRS={bin_dirs}",
            f"-DCRYPTO_BIN_DIRS={bin_dirs}",
            f"-DZLIB_BIN_DIRS={bin_dirs}",
            "-DCRYPTO_LIBRARIES=libcrypto",
            "-DBUILD_EXAMPLES=OFF",
            "-DBUILD_MANPAGES=OFF",
            "-DBUILD_TESTS=OFF",
            "-DBUILD_TOOLS=OFF",
            "-DBUILD_STATIC_LIBS=OFF",
        ]

        CmakeProject.build(self, cmake_params=cmake_params, use_ninja=True)
        self.install(rf"output\{arch}\static\* .")
