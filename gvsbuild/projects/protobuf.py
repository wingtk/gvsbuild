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
class Protobuf(Tarball, CmakeProject):
    def __init__(self):
        Project.__init__(
            self,
            "protobuf",
            version="25.1",
            archive_url="https://github.com/protocolbuffers/protobuf/releases/download/v{version}/protobuf-{version}.tar.gz",
            hash="9bd87b8280ef720d3240514f884e56a712f2218f0d693b48050c836028940a42",
            dependencies=[
                "abseil-cpp",
                "cmake",
                "zlib",
                "ninja",
            ],
        )

    def build(self):
        # We need to compile with STATIC_RUNTIME off since protobuf-c also compiles with it OFF
        CmakeProject.build(
            self,
            cmake_params=r'-DBUILD_SHARED_LIBS=ON -Dprotobuf_ABSL_PROVIDER=package -Dprotobuf_DEBUG_POSTFIX="" -Dprotobuf_BUILD_TESTS=OFF -Dprotobuf_WITH_ZLIB=ON -Dprotobuf_MSVC_STATIC_RUNTIME=OFF',
            use_ninja=True,
        )

        self.install(r".\LICENSE share\doc\protobuf")


@project_add
class ProtobufC(Tarball, CmakeProject):
    def __init__(self):
        Project.__init__(
            self,
            "protobuf-c",
            version="1.5.0",
            archive_url="https://github.com/protobuf-c/protobuf-c/releases/download/v{version}/protobuf-c-{version}.tar.gz",
            hash="7b404c63361ed35b3667aec75cc37b54298d56dd2bcf369de3373212cc06fd98",
            dependencies=[
                "abseil-cpp",
                "cmake",
                "protobuf",
                "ninja",
            ],
            patches=[
                "0001-CMakeList.txt-Remove-double-dashes.patch",
            ],
        )

    def build(self):
        CmakeProject.build(
            self,
            cmake_params="-DBUILD_SHARED_LIBS=ON",
            use_ninja=True,
            source_part="build-cmake",
        )

        self.install(r".\LICENSE share\doc\protobuf-c")
        self.install_pc_files()
