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
class Libpanel(Tarball, Meson):
    def __init__(self):
        Project.__init__(
            self,
            "libpanel",
            repository="https://gitlab.gnome.org/GNOME/libpanel",
            version="1.6.0",
            archive_url="https://download.gnome.org/sources/libpanel/{major}.{minor}/libpanel-{version}.tar.xz",
            hash="b773494a3c69300345cd8e27027448d1189183026cc137802f886417c6ea30b6",
            dependencies=[
                "ninja",
                "meson",
                "msys2",
                "pkgconf",
                "glib",
                "gtk4",
                "libadwaita",
            ],
        )
        gir = "disabled"
        if self.opts.enable_gi:
            self.add_dependency("gobject-introspection")
            gir = "enabled"

        self.add_param(f"-Dintrospection={gir}")
        self.add_param("-Dvapi=false")
        self.add_param("-Ddocs=disabled")

    def build(self, **kwargs):
        Meson.build(self)
        self.install(r".\COPYING share\doc\libpanel")
