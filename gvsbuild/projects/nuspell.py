#  Copyright (C) 2025 The Gvsbuild Authors
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
class Nuspell(Tarball, CmakeProject):
    def __init__(self):
        Project.__init__(
            self,
            "nuspell",
            version="5.1.6",
            repository="https://github.com/nuspell/nuspell",
            archive_url="https://github.com/nuspell/nuspell/archive/v{version}.tar.gz",
            archive_filename="nuspell-{version}.tar.gz",
            hash="5d4baa1daf833a18dc06ae0af0571d9574cc849d47daff6b9ce11dac0a5ded6a",
            dependencies=["cmake", "ninja", "icu"],
        )

    def build(self):
        cmake_params = (
            f"-DCMAKE_INSTALL_PREFIX={self.builder.gtk_dir} "
            "-DBUILD_SHARED_LIBS=ON -DBUILD_TESTING=OFF -DBUILD_DOCS=OFF "
            f"-DBUILD_TOOLS=OFF -DICU_ROOT={self.builder.gtk_dir}"
        )
        CmakeProject.build(self, use_ninja=True, cmake_params=cmake_params)

        self.install(r".\COPYING*", r".\share\doc\nuspell")
