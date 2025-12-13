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
class LibjpegTurbo(Tarball, CmakeProject):
    def __init__(self):
        Project.__init__(
            self,
            "libjpeg-turbo",
            version="3.1.3",
            repository="https://github.com/libjpeg-turbo/libjpeg-turbo",
            archive_url="https://github.com/libjpeg-turbo/libjpeg-turbo/releases/download/{version}/libjpeg-turbo-{version}.tar.gz",
            hash="075920b826834ac4ddf97661cc73491047855859affd671d52079c6867c1c6c0",
            dependencies=[
                "cmake",
                "ninja",
                "nasm",
            ],
        )

    def build(self):
        # Keeping the env var support might be slow:
        # https://github.com/libjpeg-turbo/libjpeg-turbo/issues/600
        self.builder.mod_env("CMAKE_C_FLAGS", "-DNO_GETENV")
        CmakeProject.build(self, use_ninja=True)

        self.install(r".\LICENSE.md share\doc\libjpeg-turbo")
