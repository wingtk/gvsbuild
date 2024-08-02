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
from gvsbuild.utils.base_project import project_add


@project_add
class Lz4(Tarball, Meson):
    def __init__(self):
        Meson.__init__(
            self,
            "lz4",
            version="1.10.0",
            archive_url="https://github.com/lz4/lz4/archive/v{version}.tar.gz",
            archive_filename="lz4-{version}.tar.gz",
            hash="537512904744b35e232912055ccf8ec66d768639ff3abe5788d90d792ec5f48b",
        )

        self.add_param("-Dossfuzz=false")

    def build(self):
        Meson.push_location(self, "build/meson")
        Meson.build(self)
        Meson.pop_location(self)

        self.install(r".\lib\LICENSE share\doc\lz4")
