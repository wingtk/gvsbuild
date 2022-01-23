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

from gvsbuild.utils.base_expanders import Tarball
from gvsbuild.utils.base_project import Project, project_add


@project_add
class Cogl(Tarball, Project):
    def __init__(self):
        Project.__init__(
            self,
            "cogl",
            archive_url="http://ftp.acc.umu.se/pub/GNOME/sources/cogl/1.22/cogl-1.22.6.tar.xz",
            hash="6d134bd3e48c067507167c001200b275997fb9c68b08b48ff038211c8c251b75",
            dependencies=["python", "glib", "cairo", "pango", "gdk-pixbuf"],
            patches=[
                "001-cogl-missing-symbols.patch",
                "002-cogl-pango-missing-symbols.patch",
            ],
        )

    def build(self):
        self.builder.mod_env(
            "INCLUDE", "{}\\include\\harfbuzz".format(self.builder.gtk_dir)
        )
        self.exec_msbuild_gen(r"build\win32", "cogl.sln", add_pars="/p:UseEnv=True")

        self.install(r".\COPYING share\doc\cogl")
