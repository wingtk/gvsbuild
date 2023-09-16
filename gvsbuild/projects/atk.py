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
from gvsbuild.utils.base_project import Project, project_add


@project_add
class Atk(Tarball, Meson):
    def __init__(self):
        Project.__init__(
            self,
            "atk",
            version="2.38.0",
            lastversion_even=True,
            repository="https://gitlab.gnome.org/GNOME/atk",
            archive_url="https://download.gnome.org/sources/atk/{major}.{minor}/atk-{version}.tar.xz",
            hash="ac4de2a4ef4bd5665052952fe169657e65e895c5057dffb3c2a810f6191a0c36",
            dependencies=[
                "ninja",
                "meson",
                "pkgconf",
                "glib",
            ],
        )
        if self.opts.enable_gi:
            self.add_dependency("gobject-introspection")

        self.add_param(f"-Dintrospection={self.opts.enable_gi}")
        self.add_param("-Ddocs=false")

    def build(self, **kwargs):
        Meson.build(self, make_tests=True)
        self.install(r".\COPYING share\doc\atk")
