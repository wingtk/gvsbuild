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
class Libpng(Tarball, CmakeProject):
    def __init__(self):
        Project.__init__(
            self,
            "libpng",
            archive_url="http://prdownloads.sourceforge.net/libpng/libpng-1.6.37.tar.xz",
            hash="505e70834d35383537b6491e7ae8641f1a4bed1876dbfe361201fc80868d88ca",
            dependencies=["cmake", "ninja", "zlib"],
        )

    def build(self):
        CmakeProject.build(self, use_ninja=True)

        self.install_pc_files()
        self.install(r"LICENSE share\doc\libpng")
