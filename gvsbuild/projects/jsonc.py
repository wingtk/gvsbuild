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

from gvsbuild.utils.base_expanders import Tarball
from gvsbuild.utils.base_project import Project, project_add


@project_add
class Jsonc(Tarball, Project):
    def __init__(self):
        Project.__init__(
            self,
            "json-c",
            archive_url="https://github.com/json-c/json-c/archive/json-c-0.12.1-20160607.tar.gz",
            hash="989e09b99ded277a0a651cd18b81fcb76885fea08769d7a21b6da39fb8a34816",
            patches=["json-c-0.12.1-20160607.patch"],
        )

    def build(self):
        self.exec_msbuild_gen(r"build\win32", "json-c.sln")

        self.install(r".\COPYING share\doc\json-c")
