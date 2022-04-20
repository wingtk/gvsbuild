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
class Protobuf(Tarball, CmakeProject):
    def __init__(self):
        Project.__init__(
            self,
            "protobuf",
            archive_url="https://github.com/protocolbuffers/protobuf/releases/download/v3.20.0/protobuf-cpp-3.20.0.tar.gz",
            hash="4cfa0276b3ba4e8bb239326213fc9acfb6ac100cdfc55aeec30a551525547f9e",
            dependencies=[
                "cmake",
                "zlib",
                "ninja",
            ],
        )

    def build(self):
        # We need to compile with STATIC_RUNTIME off since protobuf-c also compiles with it OFF
        CmakeProject.build(
            self,
            cmake_params=r'-Dprotobuf_DEBUG_POSTFIX="" -Dprotobuf_BUILD_TESTS=OFF -Dprotobuf_WITH_ZLIB=ON -Dprotobuf_MSVC_STATIC_RUNTIME=OFF',
            use_ninja=True,
            source_part="cmake",
        )

        self.install(r".\LICENSE share\doc\protobuf")


@project_add
class ProtobufC(Tarball, CmakeProject):
    def __init__(self):
        Project.__init__(
            self,
            "protobuf-c",
            archive_url="https://github.com/protobuf-c/protobuf-c/releases/download/v1.4.0/protobuf-c-1.4.0.tar.gz",
            hash="26d98ee9bf18a6eba0d3f855ddec31dbe857667d269bc0b6017335572f85bbcb",
            dependencies=[
                "cmake",
                "protobuf",
                "ninja",
            ],
        )

    def build(self):
        CmakeProject.build(self, use_ninja=True, source_part="build-cmake")

        self.install(r".\LICENSE share\doc\protobuf-c")
        self.install_pc_files()
