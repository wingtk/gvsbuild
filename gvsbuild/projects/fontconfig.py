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

from gvsbuild.utils.base_builders import Meson
from gvsbuild.utils.base_expanders import Tarball
from gvsbuild.utils.base_project import Project, project_add


@project_add
class Fontconfig(Tarball, Meson):
    def __init__(self):
        Project.__init__(
            self,
            "fontconfig",
            version="2.16.1",
            lastversion_even=True,
            repository="https://gitlab.freedesktop.org/fontconfig/fontconfig",
            archive_url="https://gitlab.freedesktop.org/api/v4/projects/890/packages/generic/fontconfig/{version}/fontconfig-{version}.tar.xz",
            hash="f4577b62f3a909597c9fb032c6a7a2ae39649ed8ce7048b615a48f32abc0d53a",
            dependencies=["freetype", "gperf", "expat"],
        )
        self.add_param("-Dtests=disabled")

    def build(self):
        Meson.build(self)
        self.install(r".\COPYING share\doc\fontconfig")
