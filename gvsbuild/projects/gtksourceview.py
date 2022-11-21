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
class GtkSourceView4(Tarball, Meson):
    def __init__(self):
        Project.__init__(
            self,
            "gtksourceview4",
            version="4.8.4",
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
            version="5.6.1",
            archive_url="https://download.gnome.org/sources/gtksourceview/{major}.{minor}/gtksourceview-{version}.tar.xz",
            hash="659d9cc9d034a114f07e7e134ee80d77dec0497cb1516ae5369119c2fcb9da16",
            dependencies=["meson", "ninja", "gtk4", "pkgconf", "libxml2"],
        )
        if Project.opts.enable_gi:
            self.add_dependency("gobject-introspection")
        else:
            self.add_param("-Dintrospection=disabled")
        self.add_param("-Dvapi=false")

    def build(self):
        Meson.build(self)
        self.install(r".\COPYING share\doc\gtksourceview5")
