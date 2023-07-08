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
class LibjpegTurbo(Tarball, CmakeProject):
    def __init__(self):
        Project.__init__(
            self,
            "libjpeg-turbo",
            version="3.0.0",
            archive_url="https://sourceforge.net/projects/libjpeg-turbo/files/{version}/libjpeg-turbo-{version}.tar.gz",
            hash="c77c65fcce3d33417b2e90432e7a0eb05f59a7fff884022a9d931775d583bfaa",
            dependencies=[
                "cmake",
                "ninja",
                "nasm",
            ],
        )

    def build(self):
        # Keeping the env var support might be slow:
        # https://github.com/libjpeg-turbo/libjpeg-turbo/issues/600
        self.builder.mod_env("CMAKE_C_FLAGS", "-DNO_GETENV")
        CmakeProject.build(self, use_ninja=True)

        self.install(r".\LICENSE.md share\doc\libjpeg-turbo")
