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
from gvsbuild.utils.base_project import project_add


@project_add
class Opus(Tarball, CmakeProject):
    def __init__(self):
        CmakeProject.__init__(
            self,
            "opus",
            version="1.5.1",
            repository="https://github.com/xiph/opus",
            archive_url="https://downloads.xiph.org/releases/opus/opus-{version}.tar.gz",
            hash="b84610959b8d417b611aa12a22565e0a3732097c6389d19098d844543e340f85",
            dependencies=[
                "ninja",
                "cmake",
                "pkgconf",
            ],
        )

    def build(self):
        CmakeProject.build(
            self,
            use_ninja=True,
            cmake_params="-DOPUS_BUILD_SHARED_LIBRARY=ON -DOPUS_BUILD_TESTING=OFF",
        )
        self.install(r"COPYING share\doc\opus")

        # FIXME: remove once we switch back to meson
        self.install_pc_files()
