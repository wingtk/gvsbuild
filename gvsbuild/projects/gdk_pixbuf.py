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
class GdkPixbuf(Tarball, Meson):
    def __init__(self):
        Project.__init__(
            self,
            "gdk-pixbuf",
            archive_url="https://download.gnome.org/sources/gdk-pixbuf/2.42/gdk-pixbuf-2.42.8.tar.xz",
            hash="84acea3acb2411b29134b32015a5b1aaa62844b19c4b1ef8b8971c6b0759f4c6",
            dependencies=[
                "ninja",
                "pkg-config",
                "meson",
                "python",
                "libtiff-4",
                "libjpeg-turbo",
                "glib",
                "libpng",
            ],
        )
        if self.opts.enable_gi:
            self.add_dependency("gobject-introspection")
            enable_gi = "enabled"
        else:
            enable_gi = "disabled"

        self.add_param("-Dbuiltin_loaders=all")
        self.add_param(f"-Dintrospection={enable_gi}")
        self.add_param("-Dman=false")

    def build(self):
        Meson.build(self)
        self.install(r".\COPYING share\doc\gdk-pixbuf")

    def post_install(self):
        self.exec_cmd(r"%(gtk_dir)s\bin\gdk-pixbuf-query-loaders.exe --update-cache")
