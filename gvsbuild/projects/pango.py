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
            version="1.57.0",
            repository="https://gitlab.gnome.org/GNOME/pango",
            archive_url="https://download.gnome.org/sources/pango/{major}.{minor}/pango-{version}.tar.xz",
            hash="890640c841dae77d3ae3d8fe8953784b930fa241b17423e6120c7bfdf8b891e7",
            dependencies=[
                "ninja",
                "meson",
                "fontconfig",
                "freetype",
                "cairo",
                "harfbuzz",
                "fribidi",
                "glib",
            ],
            patches=[],
        )
        if self.opts.enable_gi:
            self.add_dependency("gobject-introspection")
        enable_gi = "enabled" if self.opts.enable_gi else "disabled"
        self.add_param(f"-Dintrospection={enable_gi}")
        self.add_param("-Dfreetype=enabled")
        self.add_param("-Dfontconfig=enabled")

    def build(self):
        Meson.build(self)
        self.install(r"COPYING share\doc\pango")
