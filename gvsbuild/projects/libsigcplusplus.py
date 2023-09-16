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
from gvsbuild.utils.base_builders import Meson
from gvsbuild.utils.base_expanders import Tarball
from gvsbuild.utils.base_project import project_add, Project


@project_add
class Libsigcplusplus(Tarball, Meson):
    def __init__(self):
        Project.__init__(
            self,
            "libsigc++",
            prj_dir="libsigc++",
            version="3.4.0",
            lastversion_even=True,
            repository="https://github.com/libsigcplusplus/libsigcplusplus",
            archive_url="https://github.com/libsigcplusplus/libsigcplusplus/releases/download/{version}/libsigc++-{version}.tar.xz",
            hash="02e2630ffb5ce93cd52c38423521dfe7063328863a6e96d41d765a6116b8707e",
            dependencies=[
                "meson",
                "ninja",
            ],
        )

    def build(self):
        Meson.build(
            self,
            meson_params="-Dbuild-examples=false -Dbuild-documentation=false",
        )

        self.install(r".\COPYING share\doc\libsigc++")
