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
class Libpsl(Tarball, Meson):
    def __init__(self):
        Project.__init__(
            self,
            "libpsl",
            version="0.23.3",
            repository="https://github.com/rockdaboot/libpsl",
            archive_url="https://github.com/rockdaboot/libpsl/releases/download/{version}/libpsl-{version}.tar.gz",
            hash="93941f85a1e7bd593fa94f299233cb5dfc91cd144fd9a78a6ceb75001c5b03be",
            dependencies=[
                "meson",
                "ninja",
                "pkgconf",
                "icu",
            ],
        )

        self.add_param("-Druntime=libicu")
        self.add_param("-Dbuiltin=true")

    def build(self):
        Meson.build(self)

        self.install(r".\LICENSE share\doc\libpsl")
