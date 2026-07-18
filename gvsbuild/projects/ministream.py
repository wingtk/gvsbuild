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
from gvsbuild.utils.base_expanders import Tarball
from gvsbuild.utils.base_project import Project, project_add


@project_add
class Ministream(Tarball, Meson):
    def __init__(self):
        Project.__init__(
            self,
            "ministream",
            repository="https://gitlab.gnome.org/GNOME/ministream",
            version="0.99.1",
            archive_url="https://gitlab.gnome.org/GNOME/ministream/-/archive/{version}/ministream-{version}.tar.gz",
            hash="4cd263f5b8c1e7c56a461b00fecfedc84e1eb5911ec7bf8749a76fdee5792192",
            dependencies=["meson", "glib"],
        )
        if self.opts.enable_gi:
            self.add_dependency("gobject-introspection")
        enable_gi = "enabled" if self.opts.enable_gi else "disabled"
        self.add_param(f"-Dintrospection={enable_gi}")

    def build(self):
        Meson.build(self)
        self.install(r".\COPYING share\doc\ministream")
