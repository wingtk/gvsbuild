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

from gvsbuild.utils.base_expanders import Tarball
from gvsbuild.utils.base_project import Project, project_add


@project_add
class LevelDB(Tarball, Project):
    def __init__(self):
        Project.__init__(
            self,
            "leveldb",
            version="1.20",
            archive_url="https://github.com/google/leveldb/archive/v{version}.tar.gz",
            archive_filename="leveldb-{version}.tar.gz",
            hash="f5abe8b5b209c2f36560b75f32ce61412f39a2922f7045ae764a2c23335b6664",
        )

    def build(self):
        self.exec_msbuild_gen(r"build\win32", "leveldb.sln")

        self.install(r".\LICENSE share\doc\leveldb")
