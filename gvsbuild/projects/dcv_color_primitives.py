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
            version="0.5.3",
            archive_url="https://github.com/aws/dcv-color-primitives/archive/v{version}.tar.gz",
            archive_file_name="dcv-color-primitives-{version}.tar.gz",
            hash="cacddfa40ea0321e1b67f73b0fbb66dc319bab548b025844be3f789650d60129",
            dependencies=["ninja", "meson", "pkgconf", "cargo"],
        )

    def build(self):
        Meson.build(self, make_tests=False)
        self.install(r".\LICENSE share\doc\dcv-color-primitives")
