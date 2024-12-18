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
class Icu(Tarball, Meson):
    def __init__(self):
        Meson.__init__(
            self,
            "icu",
            repository="https://github.com/unicode-org/icu",
            version="76.1",
            archive_url="https://github.com/unicode-org/icu/releases/download/release-{major}-{minor}/icu4c-{major}_{minor}-src.zip",
            hash="14a1942185dda2c5a07bd74f20a220954a7d94149fb5ef3cc782b52d9817fb3f",
            dependencies=[
                "ninja",
                "meson",
                "pkgconf",
            ],
            patches=["0001-Fix-circular-include-on-MS-Visual-Studio.patch"],
        )

    def build(self):
        Meson.build(self)
        self.install(r".\LICENSE share\doc\icu")
