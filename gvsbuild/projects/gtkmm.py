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
class Gtkmm3(Tarball, Meson):
    def __init__(self):
        Meson.__init__(
            self,
            "gtkmm3",
            prj_dir="gtkmm3",
            version="3.24.9",
            lastversion_major=3,
            lastversion_even=True,
            repository="https://gitlab.gnome.org/GNOME/gtkmm",
            archive_url="https://download.gnome.org/sources/gtkmm/{major}.{minor}/gtkmm-{version}.tar.xz",
            hash="30d5bfe404571ce566a8e938c8bac17576420eb508f1e257837da63f14ad44ce",
            dependencies=[
                "gdk-pixbuf",
                "pangomm3",
                "glibmm3",
                "libepoxy",
                "atkmm",
                "cairomm3",
                "gtk3",
            ],
        )

    def build(self):
        Meson.build(
            self,
            meson_params="-Dbuild-tests=false -Dbuild-atkmm-api=true -Dbuild-documentation=false -Dbuild-demos=false",
        )

        self.install(r".\COPYING share\doc\gtkmm3")


@project_add
class Gtkmm4(Tarball, Meson):
    def __init__(self):
        Meson.__init__(
            self,
            "gtkmm4",
            prj_dir="gtkmm4",
            version="4.16.0",
            lastversion_major=4,
            lastversion_even=True,
            repository="https://gitlab.gnome.org/GNOME/gtkmm",
            archive_url="https://download.gnome.org/sources/gtkmm/{major}.{minor}/gtkmm-{version}.tar.xz",
            hash="3b23fd3abf8fb223b00e9983b6010af2db80e38c89ab6994b8b6230aa85d60f9",
            dependencies=[
                "gdk-pixbuf",
                "pangomm4",
                "glibmm4",
                "libepoxy",
                "cairomm4",
                "gtk4",
            ],
        )

    def build(self):
        Meson.build(
            self,
            meson_params="-Dbuild-tests=false -Dbuild-demos=false",
        )

        self.install(r".\COPYING share\doc\gtkmm4")
