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

from gvsbuild.utils.base_expanders import Tarball
from gvsbuild.utils.base_project import Project, project_add


@project_add
class Clutter(Tarball, Project):
    def __init__(self):
        Project.__init__(
            self,
            "clutter",
            repository="https://gitlab.gnome.org/Archive/clutter",
            version="1.26.4",
            lastversion_even=True,
            archive_url="https://download.gnome.org/sources/clutter/{major}.{minor}/clutter-{version}.tar.xz",
            hash="8b48fac159843f556d0a6be3dbfc6b083fc6d9c58a20a49a6b4919ab4263c4e6",
            dependencies=["atk", "cogl", "json-glib"],
        )

    def build(self):
        self.builder.mod_env("INCLUDE", f"{self.builder.gtk_dir}\\include\\harfbuzz")
        self.exec_msbuild_gen(r"build\win32", "clutter.sln", add_pars="/p:UseEnv=True")

        self.install(r".\COPYING share\doc\clutter")
