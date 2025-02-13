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
class Libffi(Tarball, Meson):
    def __init__(self):
        Project.__init__(
            self,
            "libffi",
            version="3.4.7",
            archive_url="https://github.com/libffi/libffi/releases/download/v{version}/libffi-{version}.tar.gz",
            hash="138607dee268bdecf374adf9144c00e839e38541f75f24a1fcf18b78fda48b2d",
            dependencies=["ninja", "meson"],
        )

    def build(self):
        Meson.build(self, meson_params="-Dtests=false")
        self.install(r"LICENSE share\doc\libffi")
