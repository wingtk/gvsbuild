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

import glob
import os

from gvsbuild.utils.base_builders import MakeGir, Meson
from gvsbuild.utils.base_expanders import Tarball
from gvsbuild.utils.base_project import Project, project_add


class Project_gtk_base(Tarball, Project, MakeGir):
    def make_all_mo(self):
        if self.name == "gtk2":
            mo = "gtk20.mo"
        elif self.name == "gtk3":
            mo = "gtk30.mo"
        else:
            mo = "gtk40.mo"
        localedir = os.path.join(self.pkg_dir, "share", "locale")
        self.push_location(r".\po")
        for fp in glob.glob(os.path.join(self.build_dir, "po", "*.po")):
            f = os.path.basename(fp)
            lcmsgdir = os.path.join(localedir, f[:-3], "LC_MESSAGES")
            self.builder.make_dir(lcmsgdir)
            cmd = " ".join(["msgfmt", "-co", os.path.join(lcmsgdir, mo), f])
            self.builder.exec_cmd(cmd, working_dir=self._get_working_dir())
        self.pop_location()

        self.install(r".\COPYING share\doc\%s" % self.name)


@project_add
class Gtk2(Project_gtk_base):
    def __init__(self):
        Project.__init__(
            self,
            "gtk2",
            version="2.24.33",
            lastversion_major=2,
            lastversion_even=True,
            repository="https://gitlab.gnome.org/GNOME/gtk",
            archive_url="https://download.gnome.org/sources/gtk+/{major}.{minor}/gtk+-{version}.tar.xz",
            hash="ac2ac757f5942d318a311a54b0c80b5ef295f299c2a73c632f6bfb1ff49cc6da",
            dependencies=["atk", "gdk-pixbuf", "pango"],
            patches=[
                "gtk-revert-scrolldc-commit.patch",
                "gtk-bgimg.patch",
                "gtk-accel.patch",
                # https://github.com/hexchat/hexchat/issues/1007
                "gtk-multimonitor.patch",
                # https://github.com/hexchat/hexchat/issues/2077
                "0001-GDK-W32-Remove-WS_EX_LAYERED-from-an-opaque-window.patch",
            ],
        )
        if Project.opts.enable_gi:
            self.add_dependency("gobject-introspection")

    def build(self):
        self.builder.mod_env("INCLUDE", f"{self.builder.gtk_dir}\\include\\harfbuzz")
        self.exec_msbuild_gen(r"build\win32", "gtk+.sln", add_pars="/p:UseEnv=True")

        self.make_all_mo()

    def post_install(self):
        if Project.opts.enable_gi:
            self.builder.mod_env("INCLUDE", f"{self.builder.gtk_dir}\\include\\cairo")
            self.builder.mod_env(
                "INCLUDE", f"{self.builder.gtk_dir}\\include\\harfbuzz"
            )
            self.make_single_gir("gtk2", prj_dir="gtk2")


@project_add
class Gtk3(Tarball, Meson):
    def __init__(self):
        Project.__init__(
            self,
            "gtk3",
            prj_dir="gtk3",
            version="3.24.37",
            lastversion_major=3,
            lastversion_even=True,
            repository="https://gitlab.gnome.org/GNOME/gtk",
            archive_url="https://download.gnome.org/sources/gtk%2B/{major}.{minor}/gtk%2B-{version}.tar.xz",
            hash="6745f0b4c053794151fd0f0e2474b077cccff5f83e9dd1bf3d39fe9fe5fb7f57",
            dependencies=["atk", "gdk-pixbuf", "pango", "libepoxy"],
            patches=[
                "gtk_update_icon_cache.patch",
            ],
        )
        if self.opts.enable_gi:
            self.add_dependency("gobject-introspection")
            enable_gi = "true"
        else:
            enable_gi = "false"

        self.add_param(f"-Dintrospection={enable_gi}")

    def build(self):
        Meson.build(self, meson_params="-Dtests=false -Ddemos=false -Dexamples=false")

        self.install(r".\COPYING share\doc\gtk3")


@project_add
class Gtk4(Tarball, Meson):
    def __init__(self):
        Project.__init__(
            self,
            "gtk4",
            prj_dir="gtk4",
            version="4.10.1",
            lastversion_major=4,
            lastversion_even=True,
            repository="https://gitlab.gnome.org/GNOME/gtk",
            archive_url="https://download.gnome.org/sources/gtk/{major}.{minor}/gtk-{version}.tar.xz",
            hash="e8fcac04bc7715b9da667c911a5ee8f262e200d1d6a50adf23645ca8cfcd0311",
            dependencies=[
                "gdk-pixbuf",
                "pango",
                "libepoxy",
                "graphene",
                "cairo",
                "harfbuzz",
                "glib",
                "fribidi",
            ],
        )
        if self.opts.enable_gi:
            self.add_dependency("gobject-introspection")
            enable_gi = "enabled"
        else:
            enable_gi = "disabled"

        self.add_param(f"-Dintrospection={enable_gi}")

    def build(self):
        Meson.build(
            self,
            meson_params="-Dbuild-tests=false -Ddemos=false -Dbuild-examples=false -Dmedia-gstreamer=disabled",
        )

        self.install(r".\COPYING share\doc\gtk4")
