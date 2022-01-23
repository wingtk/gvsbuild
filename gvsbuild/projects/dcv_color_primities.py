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
from gvsbuild.utils.base_project import project_add


@project_add
class DcvColorPrimitives(Tarball, Meson):
    def __init__(self):
        Meson.__init__(
            self,
            "dcv-color-primitives",
            archive_url="https://github.com/aws/dcv-color-primitives/archive/v0.4.0.tar.gz",
            archive_file_name="dcv-color-primitives-0.4.0.tar.gz",
            hash="85cd76c7ec3dededb27fcb13459ca361324ef3c83f784925080a899cfd8d7349",
            dependencies=["ninja", "meson", "pkg-config", "cargo"],
        )

    def build(self):
        Meson.build(self, make_tests=False)
        self.install(r".\LICENSE share\doc\dcv-color-primitives")
