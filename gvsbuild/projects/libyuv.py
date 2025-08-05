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
from gvsbuild.utils.base_expanders import GitRepo
from gvsbuild.utils.base_project import Project, project_add


@project_add
class Libyuv(GitRepo, CmakeProject):
    def __init__(self):
        Project.__init__(
            self,
            "libyuv",
            repository="https://chromium.googlesource.com/libyuv/libyuv",
            repo_url="https://chromium.googlesource.com/libyuv/libyuv",
            fetch_submodules=False,
            tag="464c51a03",
            dependencies=[
                "cmake",
                "ninja",
                "libjpeg-turbo",
            ],
            patches=[
                "001-win-build.patch",
            ],
        )

    def build(self):
        CmakeProject.build(
            self, cmake_params=r"-DCMAKE_POLICY_VERSION_MINIMUM=3.5", use_ninja=False
        )

        self.install_pc_files()
        self.install(r".\LICENSE share\doc\libyuv")
