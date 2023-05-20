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
class Gtkmm(Tarball, Meson):
    def __init__(self):
        Meson.__init__(
            self,
            "gtkmm",
            prj_dir="gtkmm",
            version="4.10.0",
            lastversion_major=4,
            lastversion_even=True,
            repository="https://gitlab.gnome.org/GNOME/gtkmm",
            archive_url="https://download.gnome.org/sources/gtkmm/{major}.{minor}/gtkmm-{version}.tar.xz",
            hash="e1b109771557ecc53cba915a80b6ede827ffdbd0049c62fdf8bd7fa79afcc6eb",
            dependencies=[
                "gdk-pixbuf",
                "pangomm",
                "glibmm",
                "libepoxy",
                "cairomm",
                "gtk4",
            ],
        )

    def build(self):
        Meson.build(
            self,
            meson_params="-Dbuild-tests=false -Dbuild-demos=false",
        )

        self.install(r".\COPYING share\doc\gtkmm")
