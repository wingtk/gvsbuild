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
            archive_url="https://download.gnome.org/sources/atk/2.36/atk-2.36.0.tar.xz",
            hash="fb76247e369402be23f1f5c65d38a9639c1164d934e40f6a9cf3c9e96b652788",
            dependencies=[
                "ninja",
                "meson",
                "pkg-config",
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
