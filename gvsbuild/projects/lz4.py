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
class Lz4(Tarball, Project):
    def __init__(self):
        Project.__init__(
            self,
            "lz4",
            archive_url="https://github.com/lz4/lz4/archive/v1.9.3.tar.gz",
            archive_file_name="lz4-1.9.3.tar.gz",
            hash="030644df4611007ff7dc962d981f390361e6c97a34e5cbc393ddfbe019ffe2c1",
        )

    def build(self):
        self.exec_msbuild_gen(r"visual", "lz4.sln")

        self.install(
            r"visual\%(vs_ver_year)s\bin\%(platform)s_%(configuration)s\liblz4.dll visual\%(vs_ver_year)s\bin\%(platform)s_%(configuration)s\liblz4.pdb bin"
        )
        self.install(r".\lib\lz4.h .\lib\lz4hc.h .\lib\lz4frame.h include")
        self.install(
            r"visual\%(vs_ver_year)s\bin\%(platform)s_%(configuration)s\liblz4.lib lib"
        )

        self.install(r".\lib\LICENSE share\doc\lz4")
        self.install_pc_files()
