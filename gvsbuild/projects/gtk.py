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
        mo = "gtk20.mo" if self.name == "gtk" else "gtk30.mo"

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
            archive_url="https://download.gnome.org/sources/gtk+/2.24/gtk+-2.24.31.tar.xz",
            hash="68c1922732c7efc08df4656a5366dcc3afdc8791513400dac276009b40954658",
            dependencies=["atk", "gdk-pixbuf", "pango"],
            patches=[
                "gtk-revert-scrolldc-commit.patch",
                "gtk-bgimg.patch",
                "gtk-accel.patch",
                # https://github.com/hexchat/hexchat/issues/1007
                "gtk-multimonitor.patch",
                # These two will be in 2.24.33
                "bfdac2f70e005b2504cc3f4ebbdab328974d005a.patch",
                "61162225f712df648f38fd12bc0817cfa9f79a64.patch",
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
            self.make_single_gir("gtk", prj_dir="gtk")


@project_add
class Gtk320(Project_gtk_base):
    def __init__(self):
        if self.opts.gtk3_ver != "3.20":
            self.ignore()
            return

        Project.__init__(
            self,
            "gtk3",
            prj_dir="gtk3-20",
            archive_url="https://download.gnome.org/sources/gtk%2B/3.20/gtk%2B-3.20.10.tar.xz",
            hash="e81da1af1c5c1fee87ba439770e17272fa5c06e64572939814da406859e56b70",
            dependencies=["atk", "gdk-pixbuf", "pango", "libepoxy"],
            patches=["gtk3-clip-retry-if-opened-by-others.patch"],
        )
        if Project.opts.enable_gi:
            self.add_dependency("gobject-introspection")

    def build(self):
        self.builder.mod_env("INCLUDE", f"{self.builder.gtk_dir}\\include\\harfbuzz")
        self.exec_msbuild_gen(
            r"build\win32", "gtk+.sln", add_pars="/p:UseEnv=True /p:GtkPostInstall=rem"
        )

        self.make_all_mo()

    def post_install(self):
        if Project.opts.enable_gi:
            self.builder.mod_env("INCLUDE", f"{self.builder.gtk_dir}\\include\\cairo")
            self.make_single_gir("gtk", prj_dir="gtk3-20")

        self.exec_cmd(
            r"%(gtk_dir)s\bin\glib-compile-schemas.exe %(gtk_dir)s\share\glib-2.0\schemas"
        )
        self.exec_cmd(
            r'%(gtk_dir)s\bin\gtk-update-icon-cache.exe --ignore-theme-index --force "%(gtk_dir)s\share\icons\hicolor"'
        )


@project_add
class Gtk322(Project_gtk_base):
    def __init__(self):
        if self.opts.gtk3_ver != "3.22":
            self.ignore()
            return

        Project.__init__(
            self,
            "gtk3",
            prj_dir="gtk3-22",
            archive_url="https://download.gnome.org/sources/gtk%2B/3.22/gtk%2B-3.22.30.tar.xz",
            hash="a1a4a5c12703d4e1ccda28333b87ff462741dc365131fbc94c218ae81d9a6567",
            dependencies=["atk", "gdk-pixbuf", "pango", "libepoxy"],
        )
        if Project.opts.enable_gi:
            self.add_dependency("gobject-introspection")

    def build(self):
        self.builder.mod_env("INCLUDE", f"{self.builder.gtk_dir}\\include\\harfbuzz")
        self.exec_msbuild_gen(
            r"build\win32", "gtk+.sln", add_pars="/p:UseEnv=True /p:GtkPostInstall=rem"
        )

        self.make_all_mo()

    def post_install(self):
        if Project.opts.enable_gi:
            self.builder.mod_env("INCLUDE", f"{self.builder.gtk_dir}\\include\\cairo")
            self.make_single_gir("gtk", prj_dir="gtk3-22")

        self.exec_cmd(
            r"%(gtk_dir)s\bin\glib-compile-schemas.exe %(gtk_dir)s\share\glib-2.0\schemas"
        )
        self.exec_cmd(
            r'%(gtk_dir)s\bin\gtk-update-icon-cache.exe --ignore-theme-index --force "%(gtk_dir)s\share\icons\hicolor"'
        )


@project_add
class Gtk324(Tarball, Meson):
    def __init__(self):
        if self.opts.gtk3_ver != "3.24":
            self.ignore()
            return

        Project.__init__(
            self,
            "gtk3",
            prj_dir="gtk3-24",
            archive_url="https://download.gnome.org/sources/gtk%2B/3.24/gtk%2B-3.24.31.tar.xz",
            hash="423c3e7fdb4c459ee889e35fd4d71fd2623562541c1041b11c07e5ad1ff10bf9",
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
            archive_url="https://download.gnome.org/sources/gtk/4.6/gtk-4.6.1.tar.xz",
            hash="d85508d21cbbcd63d568a7862af5ecd63b978d7d5799cbe404c91d2389d0ec5f",
            dependencies=["gdk-pixbuf", "pango", "libepoxy", "graphene"],
            patches=[],
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
