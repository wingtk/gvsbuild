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
from gvsbuild.utils.base_project import Project, project_add


@project_add
class Harfbuzz(Tarball, Meson):
    def __init__(self):
        self.version = "5.3.1"
        Project.__init__(
            self,
            "harfbuzz",
            archive_url=f"https://github.com/harfbuzz/harfbuzz/releases/download/{self.version}/harfbuzz-{self.version}.tar.xz",
            hash="4a6ce097b75a8121facc4ba83b5b083bfec657f45b003cd5a3424f2ae6b4434d",
            dependencies=["meson", "cmake", "freetype", "pkg-config", "glib"],
        )

        if Project.opts.enable_gi:
            self.add_dependency("gobject-introspection")
            self.add_param("-Dintrospection=enabled")
        else:
            self.add_param("-Dintrospection=disabled")

    def build(self):
        Meson.build(self)
        self.install(r".\COPYING share\doc\harfbuzz")
