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
class Cairo(Tarball, Meson):
    def __init__(self):
        Meson.__init__(
            self,
            "cairo",
            version="1.17.8",
            archive_url="https://gitlab.freedesktop.org/cairo/cairo/-/archive/{version}/cairo-{version}.tar.gz",
            hash="b4ed6d33037171d4c6594345b42d81796f335a6995fdf5638db0d306c17a0d3e",
            dependencies=["fontconfig", "freetype", "glib", "pixman", "libpng"],
        )

    def build(self):
        Meson.build(self)
        self.install(r".\COPYING share\doc\cairo")
