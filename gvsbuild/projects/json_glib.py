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
class JsonGLib(Tarball, Meson):
    def __init__(self):
        Project.__init__(
            self,
            "json-glib",
            version="1.10.6",
            lastversion_even=True,
            repository="https://gitlab.gnome.org/GNOME/json-glib",
            archive_url="https://download.gnome.org/sources/json-glib/{major}.{minor}/json-glib-{version}.tar.xz",
            hash="77f4bcbf9339528f166b8073458693f0a20b77b7059dbc2db61746a1928b0293",
            dependencies=["meson", "ninja", "pkgconf", "glib"],
        )
        if self.opts.enable_gi:
            self.add_dependency("gobject-introspection")
            enable_gi = "enabled"
        else:
            enable_gi = "disabled"

        self.add_param("-Ddocumentation=disabled")
        self.add_param(f"-Dintrospection={enable_gi}")

    def build(self):
        Meson.build(self, make_tests=True)

        self.install(r".\LICENSES\* share\doc\json-glib")
