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

from gvsbuild.utils.base_builders import Rust
from gvsbuild.utils.base_expanders import GitRepo
from gvsbuild.utils.base_project import project_add


@project_add
class Quiche(GitRepo, Rust):
    def __init__(self):
        Rust.__init__(
            self,
            "quiche",
            repo_url="https://github.com/cloudflare/quiche",
            fetch_submodules=True,
            tag="0.4.0",
            dependencies=["cargo", "perl", "go", "nasm", "cmake", "ninja"],
            patches=["fix_boringssl_build.patch"],
        )

    def build(self):
        Rust.build(self, make_tests=True)

        self.install_pc_files()
        self.install(r".\include\quiche.h include\quiche")
        self.install(r".\cargo-build\lib\quiche.dll.lib lib\quiche")
        self.install(r".\cargo-build\lib\quiche.lib lib\quiche")
        self.install(r".\cargo-build\lib\quiche.dll bin")
        self.install(r".\cargo-build\lib\deps\quiche.pdb bin")
        self.install(r".\COPYING share\doc\quiche")
