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
class Glibmm(Tarball, Meson):
    def __init__(self):
        Meson.__init__(
            self,
            "glibmm",
            prj_dir="glibmm",
            version="2.86.0",
            lastversion_even=True,
            repository="https://gitlab.gnome.org/GNOME/glibmm",
            archive_url="https://download.gnome.org/sources/glibmm/{major}.{minor}/glibmm-{version}.tar.xz",
            hash="39c0e9f6da046d679390774efdb9ad564436236736dc2f7825e614b2d4087826",
            dependencies=[
                "meson",
                "ninja",
                "libsigc++",
                "glib",
            ],
        )

    def build(self):
        Meson.build(
            self,
            meson_params="-Dbuild-examples=false -Dbuild-documentation=false",
        )

        self.install(r".\COPYING share\doc\glibmm")


@project_add
class Glibmm2_4(Tarball, Meson):
    def __init__(self):
        Meson.__init__(
            self,
            "glibmm-2.4",
            prj_dir="glibmm-2.4",
            version="2.66.8",
            lastversion_even=True,
            repository="https://gitlab.gnome.org/GNOME/glibmm",
            archive_url="https://download.gnome.org/sources/glibmm/{major}.{minor}/glibmm-{version}.tar.xz",
            hash="64f11d3b95a24e2a8d4166ecff518730f79ecc27222ef41faf7c7e0340fc9329",
            dependencies=["meson", "ninja", "libsigc++-2.0", "glib"],
        )

    def build(self):
        Meson.build(
            self, meson_params="-Dbuild-examples=false -Dbuild-documentation=false"
        )

        self.install(r".\COPYING share\doc\glibmm-2.4")
