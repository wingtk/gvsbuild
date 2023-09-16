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
from gvsbuild.utils.base_expanders import GitRepo
from gvsbuild.utils.base_project import Project, project_add


@project_add
class BoringSSL(GitRepo, CmakeProject):
    def __init__(self):
        Project.__init__(
            self,
            "boringssl",
            repository="https://github.com/google/boringssl",
            repo_url="https://github.com/google/boringssl.git",
            fetch_submodules=False,
            tag="44b3df6f03d85c901767250329c571db405122d5",  # commit from master-with-bazel branch
            dependencies=["cmake", "go", "perl", "nasm", "ninja"],
        )

    def build(self, **kwargs):
        # If do_install is True, the build fails
        CmakeProject.build(self, use_ninja=True, do_install=False)

        self.install(r".\_gvsbuild-cmake\ssl.lib lib")
        self.install(r".\_gvsbuild-cmake\crypto.lib lib")
        self.install(r".\LICENSE share\doc\boringssl")
        self.install(r".\src\include\openssl\* include\boringssl\openssl")
