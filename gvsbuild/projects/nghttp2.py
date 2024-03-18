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
            version="1.59.0",
            archive_url="https://github.com/nghttp2/nghttp2/releases/download/v{version}/nghttp2-{version}.tar.xz",
            hash="fdc9bd71f5cf8d3fdfb63066b89364c10eb2fdeab55f3c6755cd7917b2ec4ffb",
            dependencies=[
                "cmake",
                "zlib",
                "ninja",
            ],
            patches=["0001-Define-ssize_t-if-not-defined.patch"],
        )

    def build(self):
        CmakeProject.build(self, use_ninja=True)

        self.install(r".\COPYING share\doc\nghttp2")
