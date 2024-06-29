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
class Harfbuzz(Tarball, Meson):
    def __init__(self):
        Project.__init__(
            self,
            "harfbuzz",
            version="9.0.0",
            archive_url="https://github.com/harfbuzz/harfbuzz/releases/download/{version}/harfbuzz-{version}.tar.xz",
            hash="a41b272ceeb920c57263ec851604542d9ec85ee3030506d94662067c7b6ab89e",
            dependencies=["meson", "cmake", "freetype", "cairo", "pkgconf", "glib"],
        )

        if Project.opts.enable_gi:
            self.add_dependency("gobject-introspection")
            self.add_param("-Dintrospection=enabled")
        else:
            self.add_param("-Dintrospection=disabled")

        self.add_param("-Ddirectwrite=enabled")
        self.add_param("-Dgdi=enabled")

    def build(self):
        Meson.build(self)
        self.install(r".\COPYING share\doc\harfbuzz")
