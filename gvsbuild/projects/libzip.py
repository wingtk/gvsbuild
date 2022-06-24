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

from gvsbuild.utils.base_builders import CmakeProject
from gvsbuild.utils.base_expanders import Tarball
from gvsbuild.utils.base_project import Project, project_add


@project_add
class Libzip(Tarball, CmakeProject):
    def __init__(self):
        Project.__init__(
            self,
            "libzip",
            archive_url="https://libzip.org/download/libzip-1.9.0.tar.gz",
            hash="4cab273e28d08424eaa70e3690dbda61c5ea22b3b1754f43568b33d3757fb68f",
            dependencies=["cmake", "ninja", "zlib"],
        )

    def build(self):
        CmakeProject.build(self, use_ninja=True)
        self.install(r".\LICENSE share\doc\libzip")
