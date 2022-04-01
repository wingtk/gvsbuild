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
            archive_url="https://gitlab.gnome.org/GNOME/wing/-/archive/v0.3.10/wing-v0.3.10.tar.gz",
            hash="315f6c2d89a38f111124ddd35c7e918ca1fb5792a0af6d63c208deccdc2ac4c3",
            dependencies=["ninja", "meson", "pkg-config", "glib"],
        )

    def build(self):
        Meson.build(self)
        self.install(r".\COPYING share\doc\wing")
