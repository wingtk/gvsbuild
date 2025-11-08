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
class Nghttp2(Tarball, CmakeProject):
    def __init__(self):
        Project.__init__(
            self,
            "nghttp2",
            version="1.68.0",
            repository="https://github.com/nghttp2/nghttp2",
            archive_url="https://github.com/nghttp2/nghttp2/releases/download/v{version}/nghttp2-{version}.tar.xz",
            hash="5511d3128850e01b5b26ec92bf39df15381c767a63441438b25ad6235def902c",
            dependencies=[
                "cmake",
                "zlib",
                "ninja",
            ],
            patches=[],
        )

    def build(self):
        CmakeProject.build(self, use_ninja=True)

        self.install(r".\COPYING share\doc\nghttp2")
