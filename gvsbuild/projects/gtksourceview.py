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
class GtkSourceView4(Tarball, Meson):
    def __init__(self):
        Project.__init__(
            self,
            "gtksourceview4",
            version="4.8.4",
            lastversion_major=4,
            lastversion_even=True,
            repository="https://gitlab.gnome.org/GNOME/gtksourceview",
            archive_url="https://download.gnome.org/sources/gtksourceview/{major}.{minor}/gtksourceview-{version}.tar.xz",
            hash="7ec9d18fb283d1f84a3a3eff3b7a72b09a10c9c006597b3fbabbb5958420a87d",
            dependencies=["meson", "ninja", "gtk3", "pkgconf", "libxml2"],
        )
        if Project.opts.enable_gi:
            self.add_dependency("gobject-introspection")
        else:
            self.add_param("-Dgir=false")
        self.add_param("-Dvapi=false")

    def build(self):
        Meson.build(self)
        self.install(r".\COPYING share\doc\gtksourceview4")


@project_add
class GtkSourceView5(Tarball, Meson):
    def __init__(self):
        Project.__init__(
            self,
            "gtksourceview5",
            version="5.12.1",
            lastversion_major=5,
            lastversion_even=True,
            repository="https://gitlab.gnome.org/GNOME/gtksourceview",
            archive_url="https://download.gnome.org/sources/gtksourceview/{major}.{minor}/gtksourceview-{version}.tar.xz",
            hash="84c82aad985c5aadae7cea7804904a76341ec82b268d46594c1a478f39b42c1f",
            dependencies=["meson", "ninja", "gtk4", "pkgconf", "libxml2"],
            patches=[],
        )
        if Project.opts.enable_gi:
            self.add_dependency("gobject-introspection")
        else:
            self.add_param("-Dintrospection=disabled")
        self.add_param("-Dvapi=false")

    def build(self):
        Meson.build(self)
        self.install(r".\COPYING share\doc\gtksourceview5")
