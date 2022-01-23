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

from gvsbuild.utils.base_builders import Meson
from gvsbuild.utils.base_expanders import Tarball
from gvsbuild.utils.base_project import Project, project_add


@project_add
class Wing(Tarball, Meson):
    def __init__(self):
        Project.__init__(
            self,
            "wing",
            archive_url="https://gitlab.gnome.org/GNOME/wing/-/archive/v0.3.8/wing-v0.3.8.tar.gz",
            hash="b63b8f2a267e871f0c8d2cdf4bc03688e6841989457b8f42b0f40a1c98f28cca",
            dependencies=["ninja", "meson", "pkg-config", "glib"],
        )

    def build(self):
        Meson.build(self)
        self.install(r".\COPYING share\doc\wing")
