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
class Libepoxy(Tarball, Meson):
    def __init__(self):
        Project.__init__(
            self,
            "libepoxy",
            version="1.5.10",
            archive_url="https://github.com/anholt/libepoxy/archive/refs/tags/{version}.tar.gz",
            archive_filename="libepoxy-{version}.tar.gz",
            hash="a7ced37f4102b745ac86d6a70a9da399cc139ff168ba6b8002b4d8d43c900c15",
            dependencies=["ninja", "meson"],
        )

    def build(self):
        Meson.build(self)
        self.install(r"COPYING share\doc\libepoxy")
