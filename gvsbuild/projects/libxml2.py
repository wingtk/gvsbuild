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
class Libxml2(Tarball, Meson):
    def __init__(self):
        Project.__init__(
            self,
            "libxml2",
            version="2.15.1",
            repository="https://gitlab.gnome.org/GNOME/libxml2",
            archive_url="https://download.gnome.org/sources/libxml2/{major}.{minor}/libxml2-{version}.tar.xz",
            hash="c008bac08fd5c7b4a87f7b8a71f283fa581d80d80ff8d2efd3b26224c39bc54c",
            dependencies=["win-iconv", "meson", "ninja"],
        )

    def build(self):
        Meson.build(self)
        self.install(r".\COPYING share\doc\libxml2")
