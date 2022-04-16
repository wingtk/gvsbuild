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
            archive_url="https://libarchive.org/downloads/libarchive-3.6.0.tar.xz",
            hash="df283917799cb88659a5b33c0a598f04352d61936abcd8a48fe7b64e74950de7",
            dependencies=[
                "cmake",
                "ninja",
                "win-iconv",
                "zlib",
                "lz4",
                "openssl1",
                "libxml2",
            ],
            patches=["0001-ZIP-reader-fix-possible-out-of-bounds-read-in-zipx_l.patch"],
        )

    def build(self):
        CmakeProject.build(self, cmake_params="-DENABLE_WERROR=OFF", use_ninja=True)
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
