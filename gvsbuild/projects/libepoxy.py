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
class Libepoxy(Tarball, Meson):
    def __init__(self):
        Project.__init__(
            self,
            "libepoxy",
            archive_url="https://github.com/anholt/libepoxy/releases/download/1.5.5/libepoxy-1.5.5.tar.xz",
            hash="261663db21bcc1cc232b07ea683252ee6992982276536924271535875f5b0556",
            dependencies=["python", "ninja", "meson"],
        )

    def build(self):
        Meson.build(self)

        self.install(r"COPYING share\doc\libepoxy")
