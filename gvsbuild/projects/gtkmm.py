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
class Gtkmm(Tarball, Meson):
    def __init__(self):
        Meson.__init__(
            self,
            "gtkmm",
            prj_dir="gtkmm",
            version="4.18.0",
            lastversion_major=4,
            lastversion_even=True,
            repository="https://gitlab.gnome.org/GNOME/gtkmm",
            archive_url="https://download.gnome.org/sources/gtkmm/{major}.{minor}/gtkmm-{version}.tar.xz",
            hash="2ee31c15479fc4d8e958b03c8b5fbbc8e17bc122c2a2f544497b4e05619e33ec",
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


@project_add
class Gtkmm3(Tarball, Meson):
    def __init__(self):
        Meson.__init__(
            self,
            "gtkmm3",
            prj_dir="gtkmm-3.0",
            version="3.24.10",
            lastversion_major=3,
            lastversion_even=True,
            repository="https://gitlab.gnome.org/GNOME/gtkmm",
            archive_url="https://download.gnome.org/sources/gtkmm/{major}.{minor}/gtkmm-{version}.tar.xz",
            hash="7ab7e2266808716e26c39924ace1fb46da86c17ef39d989624c42314b32b5a76",
            dependencies=[
                "gdk-pixbuf",
                "pangomm-1.4",
                "glibmm-2.4",
                "libepoxy",
                "cairomm-1.0",
                "atkmm",
                "gtk3",
            ],
        )

    def build(self):
        Meson.build(self, meson_params="-Dbuild-tests=false -Dbuild-demos=false")

        self.install(r".\COPYING share\doc\gtkmm-3.0")
