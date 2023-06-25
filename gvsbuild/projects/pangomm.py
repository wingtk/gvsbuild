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
class Pangomm(Tarball, Meson):
    def __init__(self):
        Meson.__init__(
            self,
            "pangomm",
            prj_dir="pangomm",
            version="2.50.1",
            lastversion_even=True,
            repository="https://gitlab.gnome.org/GNOME/pangomm",
            archive_url="https://download.gnome.org/sources/pangomm/{major}.{minor}/pangomm-{version}.tar.xz",
            hash="ccc9923413e408c2bff637df663248327d72822f11e394b423e1c5652b7d9214",
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
