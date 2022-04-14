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

from gvsbuild.utils.base_builders import Meson
from gvsbuild.utils.base_expanders import Tarball
from gvsbuild.utils.base_project import Project, project_add


@project_add
class Lz4(Tarball, Meson):
    def __init__(self):
        Project.__init__(
            self,
            "lz4",
            archive_url="https://github.com/lz4/lz4/archive/v1.9.3.tar.gz",
            archive_file_name="lz4-1.9.3.tar.gz",
            hash="030644df4611007ff7dc962d981f390361e6c97a34e5cbc393ddfbe019ffe2c1",
            dependencies=["ninja", "meson"],
        )
        self.add_param("-Ddefault_library=shared")

    def build(self, **kwargs):
        Meson.build(self)
        self.install(r".\lib\LICENSE share\doc\lz4")
