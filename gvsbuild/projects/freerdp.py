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
class FreeRDP(Tarball, CmakeProject):
    def __init__(self):
        Project.__init__(
            self,
            "freerdp",
            version="2.11.2",
            archive_url="https://github.com/FreeRDP/FreeRDP/files/12670558/freerdp-{version}.tar.gz",
            hash="17e36553065cb59126f8fee987ec74783db50232b361574dac86b7a768dea3b4",
            dependencies=[
                "cmake",
                "ninja",
                "openssl",
                "openh264",
                "ffmpeg",
                "x264",
                "zlib",
                "libjpeg-turbo",
            ],
        )

    def build(self):
        CmakeProject.build(
            self, use_ninja=True, cmake_params="-DWITH_SSE2=ON -DCHANNEL_URBDRC=OFF"
        )

        self.install(r".\LICENSE share\doc\freerdp")
