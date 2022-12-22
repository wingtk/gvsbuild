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
            version="1.17.6",
            archive_url="https://gitlab.freedesktop.org/cairo/cairo/-/archive/{version}/cairo-{version}.tar.gz",
            hash="a2227afc15e616657341c42af9830c937c3a6bfa63661074eabef13600e8936f",
            dependencies=["fontconfig", "freetype", "glib", "pixman", "libpng"],
            patches=[
                "0001-dwrite-toy-fonts.patch",
                "0002-fix-scaled-font-hash-lookup.patch",
            ],
        )

    def build(self):
        Meson.build(self)
        self.install(r".\COPYING share\doc\cairo")
