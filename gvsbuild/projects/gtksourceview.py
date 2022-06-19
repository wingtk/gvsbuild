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
            archive_url="https://download.gnome.org/sources/gtksourceview/4.8/gtksourceview-4.8.3.tar.xz",
            hash="c30019506320ca2474d834cced1e2217ea533e00eb2a3f4eb7879007940ec682",
            dependencies=["python", "meson", "ninja", "gtk3", "pkg-config"],
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
            archive_url="https://download.gnome.org/sources/gtksourceview/5.4/gtksourceview-5.4.2.tar.xz",
            hash="ad140e07eb841910de483c092bd4885abd29baadd6e95fa22d93ed2df0b79de7",
            dependencies=["python", "meson", "ninja", "gtk4", "pkg-config"],
        )
        if Project.opts.enable_gi:
            self.add_dependency("gobject-introspection")
        else:
            self.add_param("-Dintrospection=disabled")
        self.add_param("-Dvapi=false")

    def build(self):
        Meson.build(self)
        self.install(r".\COPYING share\doc\gtksourceview5")
