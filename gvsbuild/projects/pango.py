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
class Pango(Tarball, Meson):
    def __init__(self):
        Project.__init__(
            self,
            "pango",
            version="1.55.0",
            repository="https://gitlab.gnome.org/GNOME/pango",
            archive_url="https://download.gnome.org/sources/pango/{major}.{minor}/pango-{version}.tar.xz",
            hash="a2c17a8dc459a7267b8b167bb149d23ff473b6ff9d5972bee047807ee2220ccf",
            dependencies=[
                "ninja",
                "meson",
                "freetype",
                "cairo",
                "harfbuzz",
                "fribidi",
            ],
            patches=[],
        )
        if self.opts.enable_gi:
            self.add_dependency("gobject-introspection")
            enable_gi = "enabled"
        else:
            enable_gi = "disabled"

        self.add_param(f"-Dintrospection={enable_gi}")
        self.add_param("-Dfreetype=enabled")

    def build(self):
        Meson.build(self)
        self.install(r"COPYING share\doc\pango")
