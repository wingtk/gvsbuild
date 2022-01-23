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
            archive_url="http://ftp.acc.umu.se/pub/GNOME/sources/gdk-pixbuf/2.42/gdk-pixbuf-2.42.6.tar.xz",
            hash="c4a6b75b7ed8f58ca48da830b9fa00ed96d668d3ab4b1f723dcf902f78bde77f",
            dependencies=[
                "ninja",
                "pkg-config",
                "meson",
                "python",
                "libtiff-4",
                "glib",
                "libpng",
            ],
            patches=["115.diff"],
        )
        if self.opts.enable_gi:
            self.add_dependency("gobject-introspection")
            enable_gi = "enabled"
        else:
            enable_gi = "disabled"

        self.add_param("-Dnative_windows_loaders=true")
        self.add_param("-Dintrospection={}".format(enable_gi))
        self.add_param("-Dman=false")
        self.add_param("-Dx11=false")

    def build(self):
        # We can experiment with a couple of options to give to meson:
        #    -Dbuiltin_loaders=all|windows
        #        Buld the loader inside the library
        Meson.build(self)
        self.install(r".\COPYING share\doc\gdk-pixbuf")

    def post_install(self):
        self.exec_cmd(r"%(gtk_dir)s\bin\gdk-pixbuf-query-loaders.exe --update-cache")
