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

from gvsbuild.utils.base_builders import Meson
from gvsbuild.utils.base_expanders import GitRepo
from gvsbuild.utils.base_project import Project, project_add


@project_add
class Libadwaita(GitRepo, Meson):
    def __init__(self):
        Project.__init__(
            self,
            "libadwaita",
            repository="https://gitlab.gnome.org/sp1rit/libadwaita.git",
            fetch_submodules=False,
            tag="ministream",
            dependencies=[
                "ninja",
                "meson",
                "msys2",
                "pkgconf",
                "glib",
                "gtk4",
                "ministream",
            ],
        )
        if self.opts.enable_gi:
            self.add_dependency("gobject-introspection")
        enable_gi = "enabled" if self.opts.enable_gi else "disabled"
        self.add_param(f"-Dintrospection={enable_gi}")
        self.add_param("-Ddocumentation=false")
        self.add_param("-Dvapi=false")
        self.add_param("-Dexamples=false")
        self.add_param("-Dtests=false")

    def build(self, **kwargs):
        Meson.build(self)
        self.install(r".\COPYING share\doc\libadwaita")
