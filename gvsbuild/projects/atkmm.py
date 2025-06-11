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
class Atkmm(Tarball, Meson):
    def __init__(self):
        Meson.__init__(
            self,
            "atkmm",
            prj_dir="atkmm-1.6",
            version="2.28.4",
            lastversion_even=True,
            repository="https://gitlab.gnome.org/GNOME/atkmm",
            archive_url="https://download.gnome.org/sources/atkmm/{major}.{minor}/atkmm-{version}.tar.xz",
            hash="0a142a8128f83c001efb8014ee463e9a766054ef84686af953135e04d28fdab3",
            dependencies=["meson", "ninja", "atk", "glibmm-2.4", "libsigc++-2.0"],
        )

    def build(self):
        Meson.build(self, meson_params="-Dbuild-documentation=false")
        self.install(r".\COPYING share\doc\atkmm-1.6")
