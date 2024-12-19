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
class Pangomm3(Tarball, Meson):
    def __init__(self):
        Meson.__init__(
            self,
            "pangomm3",
            prj_dir="pangomm-1.4",
            version="2.46.4",
            repository="https://gitlab.gnome.org/GNOME/pangomm",
            archive_url="https://download.gnome.org/sources/pangomm/{major}.{minor}/pangomm-{version}.tar.xz",
            hash="b92016661526424de4b9377f1512f59781f41fb16c9c0267d6133ba1cd68db22",
            dependencies=[
                "meson",
                "ninja",
                "libsigc++3",
                "cairomm3",
                "pango",
                "glibmm3",
            ],
        )

    def build(self):
        Meson.build(
            self,
            meson_params="-Dbuild-documentation=false",
        )

        self.install(r".\COPYING share\doc\glibmm3")

@project_add
class Pangomm4(Tarball, Meson):
    def __init__(self):
        Meson.__init__(
            self,
            "pangomm4",
            prj_dir="pangomm4",
            version="2.54.0",
            lastversion_even=True,
            repository="https://gitlab.gnome.org/GNOME/pangomm",
            archive_url="https://download.gnome.org/sources/pangomm/{major}.{minor}/pangomm-{version}.tar.xz",
            hash="4a5b1fd1b7c47a1af45277ea82b5abeaca8e08fb10a27daa6394cf88d74e7acf",
            dependencies=[
                "meson",
                "ninja",
                "libsigc++4",
                "cairomm4",
                "pango",
                "glibmm4",
            ],
        )

    def build(self):
        Meson.build(
            self,
            meson_params="-Dbuild-documentation=false",
        )

        self.install(r".\COPYING share\doc\glibmm4")
