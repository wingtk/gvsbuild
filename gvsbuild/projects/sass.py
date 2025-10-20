#  Copyright (C) 2025 The Gvsbuild Authors
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
class Libsass(Tarball, Meson):
    def __init__(self):
        Project.__init__(
            self,
            "libsass",
            version="3.6.6",
            archive_url="https://github.com/sass/libsass/archive/refs/tags/{version}.tar.gz",
            hash="11f0bb3709a4f20285507419d7618f3877a425c0131ea8df40fe6196129df15d",
            archive_filename="libsass-{version}.tar.gz",
            dependencies=["ninja", "meson"],
        )

    def build(self):
        Meson.build(self)
        self.install(r"LICENSE share\doc\libsass")


@project_add
class Sassc(Tarball, Meson):
    def __init__(self):
        Project.__init__(
            self,
            "sassc",
            version="3.6.2",
            archive_url="https://github.com/sass/sassc/archive/refs/tags/{version}.tar.gz",
            hash="608dc9002b45a91d11ed59e352469ecc05e4f58fc1259fc9a9f5b8f0f8348a03",
            archive_filename="sassc-{version}.tar.gz",
            dependencies=["ninja", "meson", "libsass"],
        )

    def build(self):
        Meson.build(self)
        self.install(r"LICENSE share\doc\sassc")
