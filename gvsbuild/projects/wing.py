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
class Wing(Tarball, Meson):
    def __init__(self):
        Project.__init__(
            self,
            "wing",
            version="0.3.22",
            repository="https://gitlab.gnome.org/GNOME/wing",
            archive_url="https://gitlab.gnome.org/GNOME/wing/-/archive/v{version}/wing-v{version}.tar.gz",
            hash="7c266e4745c4bc2daf8d4b84ad83ae6bf5b8f75f60f4ab70d980ed087e623527",
            dependencies=["ninja", "meson", "pkgconf", "glib"],
        )

    def build(self):
        Meson.build(self)
        self.install(r".\COPYING share\doc\wing")
