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
            version="4.5.1",
            repository="https://gitlab.com/libtiff/libtiff",
            archive_url="http://download.osgeo.org/libtiff/tiff-{version}.tar.gz",
            hash="d7f38b6788e4a8f5da7940c5ac9424f494d8a79eba53d555f4a507167dca5e2b",
            dependencies=["cmake", "ninja", "libjpeg-turbo"],
            patches=[
                "0001-cmake-remove-.d-postfix.patch",
            ],
        )

    def build(self):
        CmakeProject.build(self, use_ninja=True)

        self.install(r".\COPYRIGHT share\doc\tiff")
