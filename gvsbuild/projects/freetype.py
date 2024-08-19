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
class Freetype(Tarball, Meson):
    def __init__(self):
        Project.__init__(
            self,
            "freetype",
            version="2.13.3",
            repository="https://gitlab.freedesktop.org/freetype/freetype",
            archive_url="https://gitlab.freedesktop.org/freetype/freetype/-/archive/VER-{major}-{minor}-{micro}/freetype-VER-{major}-{minor}-{micro}.tar.gz",
            hash="bc5c898e4756d373e0d991bab053036c5eb2aa7c0d5c67e8662ddc6da40c4103",
            dependencies=["pkgconf", "ninja", "libpng"],
            patches=["0001-meson-in-shared-libraries-we-need-to-export-the-meth.patch"],
        )

    def build(self):
        Meson.build(self)
        self.install(r".\docs\LICENSE.TXT share\doc\freetype")
