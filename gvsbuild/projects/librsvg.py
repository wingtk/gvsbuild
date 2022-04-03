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

from gvsbuild.utils.base_builders import MakeGir
from gvsbuild.utils.base_expanders import Tarball
from gvsbuild.utils.base_project import Project, project_add


@project_add
class LibrsvgLegacy(Tarball, Project, MakeGir):
    def __init__(self):

        if not self.opts.old_rsvg:
            self.ignore()
            return

        Project.__init__(
            self,
            "librsvg",
            prj_dir="librsvg-legacy",
            archive_url="https://download.gnome.org/sources/librsvg/2.40/librsvg-2.40.20.tar.xz",
            hash="cff4dd3c3b78bfe99d8fcfad3b8ba1eee3289a0823c0e118d78106be6b84c92b",
            dependencies=["libcroco", "cairo", "pango", "gdk-pixbuf", "gtk3"],
            patches=["vs2019-support.patch"],
        )
        if Project.opts.enable_gi:
            self.add_dependency("gobject-introspection")

    def build(self):
        self.builder.mod_env("INCLUDE", f"{self.builder.gtk_dir}\\include\\harfbuzz")
        self.exec_msbuild_gen(r"build\win32", "librsvg.sln", add_pars="/p:UseEnv=True")

        if Project.opts.enable_gi:
            self.builder.mod_env(
                "INCLUDE", f"{self.builder.gtk_dir}\\include\\glib-2.0"
            )
            self.builder.mod_env(
                "INCLUDE", f"{self.builder.gtk_dir}\\lib\\glib-2.0\\include"
            )
            self.builder.mod_env(
                "INCLUDE", f"{self.builder.gtk_dir}\\include\\gdk-pixbuf-2.0"
            )
            self.builder.mod_env("INCLUDE", f"{self.builder.gtk_dir}\\include\\cairo")

            self.make_single_gir("rsvg", prj_dir="librsvg-legacy")

        self.install(r".\COPYING share\doc\librsvg")

    def post_install(self):
        self.exec_cmd(r"%(gtk_dir)s\bin\gdk-pixbuf-query-loaders.exe --update-cache")


@project_add
class Librsvg(Tarball, Project):
    def __init__(self):

        if self.opts.old_rsvg:
            self.ignore()
            return

        Project.__init__(
            self,
            "librsvg",
            archive_url="https://download.gnome.org/sources/librsvg/2.54/librsvg-2.54.0.tar.xz",
            hash="baf8ebc147f146b4261bb3d0cd0fac944bf8dbb4b1f2347d23341f974dcc3085",
            dependencies=[
                "cargo",
                "cairo",
                "pango",
                "gdk-pixbuf",
            ],
            patches=[],
        )
        if Project.opts.enable_gi:
            self.add_dependency("gobject-introspection")

    def build(self):
        self.builder.mod_env("INCLUDE", "include\\cairo", add_gtk=True)

        b_dir = f"{self.builder.working_dir}\\{self.name}\\win32"

        cmd = f'nmake -f makefile.vc CFG={self.builder.opts.configuration} PREFIX={self.builder.gtk_dir} PYTHON={Project.get_tool_executable("python")} install'

        if Project.opts.enable_gi:
            cmd += " INTROSPECTION=1"

        self.push_location(b_dir)
        self.exec_vs(cmd)
        self.pop_location()

        self.install(r".\COPYING.LIB share\doc\librsvg")

    def post_install(self):
        self.exec_cmd(r"%(gtk_dir)s\bin\gdk-pixbuf-query-loaders.exe --update-cache")
