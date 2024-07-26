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
class Libxml2(Tarball, Meson):
    def __init__(self):
        Project.__init__(
            self,
            "libxml2",
            version="2.12.9",
            lastversion_even=True,
            repository="https://gitlab.gnome.org/GNOME/libxml2",
            archive_url="https://download.gnome.org/sources/libxml2/{major}.{minor}/libxml2-{version}.tar.xz",
            hash="59912db536ab56a3996489ea0299768c7bcffe57169f0235e7f962a91f483590",
            dependencies=["win-iconv", "meson", "ninja"],
            patches=[],
        )

    def build(self):
        Meson.build(self)
        self.install_pc_files()
        self.install(r".\COPYING share\doc\libxml2")
