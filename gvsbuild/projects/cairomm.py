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
class Cairomm3(Tarball, Meson):
    def __init__(self):
        Meson.__init__(
            self,
            "cairomm3",
            prj_dir="cairomm-1.0",
            version="1.14.5",
            archive_url="https://gitlab.freedesktop.org/cairo/cairomm/-/archive/{version}/cairomm-{version}.tar.gz",
            hash="80c10611888e84c3a660eea0dafc81b6a9faf3e1d1cc31f950c51b3f7d384fc2",
            dependencies=["meson", "ninja", "libsigc++3", "cairo"],
        )

    def build(self):
        Meson.build(
            self, meson_params="-Dbuild-examples=false -Dbuild-documentation=false"
        )
        self.install(r".\COPYING share\doc\cairomm3")


@project_add
class Cairomm4(Tarball, Meson):
    def __init__(self):
        Meson.__init__(
            self,
            "cairomm4",
            version="1.16.2",
            archive_url="https://gitlab.freedesktop.org/cairo/cairomm/-/archive/{version}/cairomm-{version}.tar.gz",
            hash="54da2d1b51c62d9503599031979e3f132fcd6c4d507b37bd244364a0f9c692cf",
            dependencies=["meson", "ninja", "libsigc++4", "cairo"],
        )

    def build(self):
        Meson.build(
            self, meson_params="-Dbuild-examples=false -Dbuild-documentation=false"
        )
        self.install(r".\COPYING share\doc\cairomm4")
