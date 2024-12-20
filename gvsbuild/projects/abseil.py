#  Copyright (C) 2024 The Gvsbuild Authors
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
            version="20240722.0",
            archive_url="https://github.com/abseil/abseil-cpp/archive/refs/tags/{version}.tar.gz",
            archive_filename="abseil-cpp-v{version}.tar.gz",
            hash="f50e5ac311a81382da7fa75b97310e4b9006474f9560ac46f54a9967f07d4ae3",
            dependencies=[
                "cmake",
                "ninja",
                "zlib",
            ],
        )

    def build(self):
        CmakeProject.build(
            self,
            cmake_params=r"-DBUILD_SHARED_LIBS=ON -DABSL_PROPAGATE_CXX_STD=ON",
            use_ninja=True,
        )
