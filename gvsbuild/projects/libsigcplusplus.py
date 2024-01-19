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
from gvsbuild.utils.base_project import Project, project_add


@project_add
class Libsigcplusplus(Tarball, Meson):
    def __init__(self):
        Project.__init__(
            self,
            "libsigc++",
            prj_dir="libsigc++",
            version="3.6.0",
            lastversion_even=True,
            repository="https://github.com/libsigcplusplus/libsigcplusplus",
            archive_url="https://github.com/libsigcplusplus/libsigcplusplus/releases/download/{version}/libsigc++-{version}.tar.xz",
            hash="c3d23b37dfd6e39f2e09f091b77b1541fbfa17c4f0b6bf5c89baef7229080e17",
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
