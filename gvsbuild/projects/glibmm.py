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
class Glibmm3(Tarball, Meson):
    def __init__(self):
        Meson.__init__(
            self,
            "glibmm3",
            prj_dir="glibmm-2.4",
            version="2.66.7",
            lastversion_even=True,
            repository="https://gitlab.gnome.org/GNOME/glibmm",
            archive_url="https://download.gnome.org/sources/glibmm/{major}.{minor}/glibmm-{version}.tar.xz",
            hash="fe02c1e5f5825940d82b56b6ec31a12c06c05c1583cfe62f934d0763e1e542b3",
            dependencies=[
                "meson",
                "ninja",
                "libsigc++3",
                "glib",
            ],
        )

    def build(self):
        Meson.build(
            self,
            meson_params="-Dbuild-examples=false -Dbuild-documentation=false",
        )

        self.install(r".\COPYING share\doc\glibmm3")

@project_add
class Glibmm4(Tarball, Meson):
    def __init__(self):
        Meson.__init__(
            self,
            "glibmm4",
            prj_dir="glibmm4",
            version="2.82.0",
            lastversion_even=True,
            repository="https://gitlab.gnome.org/GNOME/glibmm",
            archive_url="https://download.gnome.org/sources/glibmm/{major}.{minor}/glibmm-{version}.tar.xz",
            hash="38684cff317273615c67b8fa9806f16299d51e5506d9b909bae15b589fa99cb6",
            dependencies=[
                "meson",
                "ninja",
                "libsigc++4",
                "glib",
            ],
        )

    def build(self):
        Meson.build(
            self,
            meson_params="-Dbuild-examples=false -Dbuild-documentation=false",
        )

        self.install(r".\COPYING share\doc\glibmm4")
