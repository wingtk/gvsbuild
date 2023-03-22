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
import sys

from gvsbuild.utils.base_expanders import Tarball
from gvsbuild.utils.base_project import Project, project_add


@project_add
class Librsvg(Tarball, Project):
    def __init__(self):
        Project.__init__(
            self,
            "librsvg",
            version="2.56.0",
            lastversion_even=True,
            repository="https://gitlab.gnome.org/GNOME/librsvg",
            archive_url="https://download.gnome.org/sources/librsvg/{major}.{minor}/librsvg-{version}.tar.xz",
            hash="194b5097d9cd107495f49c291cf0da65ec2b4bb55e5628369751a3f44ba222b3",
            dependencies=[
                "cargo",
                "cairo",
                "pango",
                "gdk-pixbuf",
                "libxml2",
            ],
            patches=[],
        )
        if Project.opts.enable_gi:
            self.add_dependency("gobject-introspection")

    def build(self):
        self.builder.mod_env("INCLUDE", "include\\cairo", add_gtk=True)

        b_dir = f"{self.builder.working_dir}\\{self.name}\\win32"

        cmd = f"nmake -f makefile.vc CFG={self.builder.opts.configuration} PREFIX={self.builder.gtk_dir} PYTHON={sys.executable} install"

        if Project.opts.enable_gi:
            cmd += " INTROSPECTION=1"

        self.push_location(b_dir)
        self.exec_vs(cmd)
        self.pop_location()

        self.install(r".\COPYING.LIB share\doc\librsvg")

    def post_install(self):
        self.exec_cmd(r"%(gtk_dir)s\bin\gdk-pixbuf-query-loaders.exe --update-cache")
