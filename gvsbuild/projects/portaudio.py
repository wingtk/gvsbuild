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
class Portaudio(Tarball, CmakeProject):
    def __init__(self):
        Project.__init__(
            self,
            "portaudio",
            version="19.7.0",
            archive_url="https://github.com/PortAudio/portaudio/archive/refs/tags/v{version}.tar.gz",
            archive_file_name="portaudio-{version}.tar.gz",
            hash="5af29ba58bbdbb7bbcefaaecc77ec8fc413f0db6f4c4e286c40c3e1b83174fa0",
            dependencies=[
                "cmake",
                "ninja",
            ],
        )

    def build(self):
        CmakeProject.build(
            self,
            cmake_params="-DPA_DLL_LINK_WITH_STATIC_RUNTIME=off",
            use_ninja=True,
            out_of_source=False,
        )
