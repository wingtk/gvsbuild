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
            version="1.5.2",
            repository="https://github.com/xiph/opus",
            archive_url="https://downloads.xiph.org/releases/opus/opus-{version}.tar.gz",
            hash="65c1d2f78b9f2fb20082c38cbe47c951ad5839345876e46941612ee87f9a7ce1",
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
