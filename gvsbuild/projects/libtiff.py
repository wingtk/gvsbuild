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
class Libtiff4(Tarball, CmakeProject):
    def __init__(self):
        Project.__init__(
            self,
            "libtiff-4",
            archive_url="http://download.osgeo.org/libtiff/tiff-4.4.0.tar.gz",
            hash="917223b37538959aca3b790d2d73aa6e626b688e02dcda272aec24c2f498abed",
            dependencies=[
                "cmake",
                "ninja",
                "libjpeg-turbo"
            ]
        )

    def build(self):
        CmakeProject.build(self, use_ninja=True)

        self.install(r".\COPYRIGHT share\doc\tiff")
