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

from gvsbuild.utils.base_builders import CmakeProject
from gvsbuild.utils.base_expanders import Tarball
from gvsbuild.utils.base_project import Project, project_add


@project_add
class LevelDB(Tarball, CmakeProject):
    def __init__(self):
        Project.__init__(
            self,
            "leveldb",
            version="1.23",
            archive_url="https://github.com/google/leveldb/archive/tags/{version}.tar.gz",
            archive_filename="leveldb-{version}.tar.gz",
            hash="fa183b494f3ffe418a6804a57dfc0670080fbb0bcd1949cc4527d9b0077887a8",
            dependencies=[
                "cmake",
            ],
        )

    def build(self):
        CmakeProject.build(
            self,
            use_ninja=True,
            cmake_params="-DLEVELDB_BUILD_TESTS=OFF -DLEVELDB_BUILD_BENCHMARKS=OFF",
        )

        self.install(r".\LICENSE share\doc\leveldb")
