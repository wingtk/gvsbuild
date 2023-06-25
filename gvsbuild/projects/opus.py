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
from gvsbuild.utils.base_project import project_add


@project_add
class Opus(Tarball, Meson):
    def __init__(self):
        Meson.__init__(
            self,
            "opus",
            version="1.4",
            repository="https://github.com/xiph/opus",
            archive_url="https://github.com/xiph/opus/releases/download/v{version}/opus-{version}.tar.gz",
            hash="c9b32b4253be5ae63d1ff16eea06b94b5f0f2951b7a02aceef58e3a3ce49c51f",
            dependencies=[
                "ninja",
                "meson",
                "pkgconf",
            ],
        )

        self.add_param("-Dtests=disabled")
        self.add_param("-Ddocs=disabled")

    def build(self):
        Meson.build(self)
        self.install(r"COPYING share\doc\opus")
