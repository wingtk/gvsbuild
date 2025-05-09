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
class Libpng(Tarball, CmakeProject):
    def __init__(self):
        Project.__init__(
            self,
            "libpng",
            version="1.6.48",
            repository="https://github.com/pnggroup/libpng",
            archive_url="https://github.com/pnggroup/libpng/archive/v{version}.tar.gz",
            archive_filename="libpng-{version}.tar.gz",
            hash="b17e99026055727e8cba99160c3a9a7f9af788e9f786daeadded5a42243f1dd0",
            dependencies=["cmake", "ninja", "zlib"],
        )

    def build(self):
        cmake_params = '-DPNG_TOOLS=OFF -DPNG_TESTS=OFF -Dld-version-script=OFF -DPNG_DEBUG_POSTFIX=""'
        CmakeProject.build(self, cmake_params=cmake_params, use_ninja=True)

        self.install_pc_files()
        self.install(r"LICENSE share\doc\libpng")
