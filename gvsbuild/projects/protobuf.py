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
            version="3.21.12",
            lastversion_major=3,
            archive_url="https://github.com/protocolbuffers/protobuf/releases/download/v{minor}.{micro}/protobuf-cpp-{version}.tar.gz",
            hash="4eab9b524aa5913c6fffb20b2a8abf5ef7f95a80bc0701f3a6dbb4c607f73460",
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
            cmake_params=r'-DBUILD_SHARED_LIBS=ON -Dprotobuf_DEBUG_POSTFIX="" -Dprotobuf_BUILD_TESTS=OFF -Dprotobuf_WITH_ZLIB=ON -Dprotobuf_MSVC_STATIC_RUNTIME=OFF',
            use_ninja=True,
        )

        self.install(r".\LICENSE share\doc\protobuf")


@project_add
class ProtobufC(Tarball, CmakeProject):
    def __init__(self):
        Project.__init__(
            self,
            "protobuf-c",
            version="1.4.1",
            archive_url="https://github.com/protobuf-c/protobuf-c/releases/download/v{version}/protobuf-c-{version}.tar.gz",
            hash="4cc4facd508172f3e0a4d3a8736225d472418aee35b4ad053384b137b220339f",
            dependencies=[
                "cmake",
                "protobuf",
                "ninja",
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
