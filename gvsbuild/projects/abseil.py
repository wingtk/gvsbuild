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
class AbseilCpp(Tarball, CmakeProject):
    def __init__(self):
        Project.__init__(
            self,
            "abseil-cpp",
            version="20240116.1",
            archive_url="https://github.com/abseil/abseil-cpp/archive/refs/tags/{version}.tar.gz",
            archive_file_name="abseil-cpp-{version}.tar.gz",
            hash="3c743204df78366ad2eaf236d6631d83f6bc928d1705dd0000b872e53b73dc6a",
            dependencies=["cmake", "ninja"],
        )

    def build(self, **kwargs):
        CmakeProject.build(
            self,
            use_ninja=True,
            cmake_params=r"-DABSL_PROPAGATE_CXX_STD=ON -DABSL_BUILD_DLL=ON",
        )

        self.install(r".\LICENSE share\doc\abseil-cpp")
