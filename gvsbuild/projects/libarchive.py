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
from gvsbuild.utils.utils import file_replace


@project_add
class Libarchive(Tarball, CmakeProject):
    def __init__(self):
        Project.__init__(
            self,
            "libarchive",
            version="3.8.1",
            archive_url="https://libarchive.org/downloads/libarchive-{version}.tar.xz",
            hash="19f917d42d530f98815ac824d90c7eaf648e9d9a50e4f309c812457ffa5496b5",
            dependencies=[
                "cmake",
                "ninja",
                "win-iconv",
                "zlib",
                "lz4",
                "openssl",
                "libxml2",
            ],
            patches=[
                # https://github.com/libarchive/libarchive/pull/2676
                "001-fix-wrong-pkgconfig-path.patch",
            ],
        )

    def build(self):
        cmake_params = (
            "-DENABLE_WERROR=OFF -DENABLE_TEST=OFF -DBUILD_TESTING=OFF -Wno-dev"
        )
        CmakeProject.build(self, cmake_params=cmake_params, use_ninja=True)
        # Fix the pkg-config .pc file, correcting the library's names
        file_replace(
            os.path.join(self.pkg_dir, "lib", "pkgconfig", "libarchive.pc"),
            [
                (" -llz4", " -lliblz4"),
                (" -leay32", " -llibeay32"),
                (" -lxml2", " -llibxml2"),
            ],
        )
        self.install(r".\COPYING share\doc\libarchive")
