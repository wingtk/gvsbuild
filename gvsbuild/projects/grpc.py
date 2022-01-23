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
from gvsbuild.utils.base_expanders import GitRepo
from gvsbuild.utils.base_project import Project, project_add


@project_add
class Grpc(GitRepo, CmakeProject):
    def __init__(self):
        Project.__init__(
            self,
            "grpc",
            repo_url="https://github.com/grpc/grpc.git",
            fetch_submodules=True,
            tag="v1.12.0",
            dependencies=["go", "nuget", "protobuf", "perl", "zlib", "nasm"],
            patches=["0001-removing-extra-plugins.patch"],
        )

    def build(self):
        CmakeProject.build(
            self,
            cmake_params="-DgRPC_ZLIB_PROVIDER=package -DgRPC_PROTOBUF_PROVIDER=package",
            use_ninja=True,
            out_of_source=False,
        )
        self.install(r".\third_party\boringssl\ssl\ssl.lib lib")
        self.install(r".\third_party\boringssl\crypto\crypto.lib lib")
        self.install(r".\gpr.lib lib")
        self.install(r".\grpc.lib lib")
        self.install(r".\grpc++.lib lib")
        self.install(r".\grpc_cpp_plugin.exe bin")
        self.install(r".\grpc_cpp_plugin.pdb bin")
        self.install(r".\grpc_csharp_plugin.exe bin")
        self.install(r".\grpc_csharp_plugin.pdb bin")
        self.install(r".\LICENSE share\doc\grpc")
