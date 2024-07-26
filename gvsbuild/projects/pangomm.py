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
class Pangomm(Tarball, Meson):
    def __init__(self):
        Meson.__init__(
            self,
            "pangomm",
            prj_dir="pangomm",
            version="2.54.0",
            lastversion_even=True,
            repository="https://gitlab.gnome.org/GNOME/pangomm",
            archive_url="https://download.gnome.org/sources/pangomm/{major}.{minor}/pangomm-{version}.tar.xz",
            hash="4a5b1fd1b7c47a1af45277ea82b5abeaca8e08fb10a27daa6394cf88d74e7acf",
            dependencies=[
                "meson",
                "ninja",
                "libsigc++",
                "cairomm",
                "pango",
                "glibmm",
            ],
        )

    def build(self):
        Meson.build(
            self,
            meson_params="-Dbuild-documentation=false",
        )

        self.install(r".\COPYING share\doc\glibmm")
