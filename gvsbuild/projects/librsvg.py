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
class Librsvg(Tarball, Meson):
    def __init__(self):
        Project.__init__(
            self,
            "librsvg",
            version="2.61.0",
            repository="https://gitlab.gnome.org/GNOME/librsvg",
            archive_url="https://download.gnome.org/sources/librsvg/{major}.{minor}/librsvg-{version}.tar.xz",
            hash="dbd0db40a1179a382fbb8cc930837671b973d722ba106a3dee2aad0fd858e2c4",
            dependencies=[
                "cargo",
                "cairo",
                "pango",
                "gdk-pixbuf",
                "libxml2",
                "freetype",
            ],
        )

        if self.opts.enable_gi:
            self.add_dependency("gobject-introspection")
            enable_gi = "enabled"
        else:
            enable_gi = "disabled"

        self.add_param(f"-Dintrospection={enable_gi}")
        self.add_param("-Ddocs=disabled")
        self.add_param("-Dtests=false")
        self.add_param("-Dvala=disabled")

    def build(self):
        self.builder.exec_cargo("install cargo-c --locked")
        Meson.build(self)
        self.install(r".\COPYING.LIB share\doc\librsvg")

    def post_install(self):
        self.exec_cmd(r"%(gtk_dir)s\bin\gdk-pixbuf-query-loaders.exe --update-cache")
