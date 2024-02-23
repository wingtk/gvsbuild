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
class OpenH264(Tarball, Meson):
    def __init__(self):
        Project.__init__(
            self,
            "openh264",
            version="2.4.1",
            archive_url="https://github.com/cisco/openh264/archive/refs/tags/v{version}.tar.gz",
            archive_filename="openh264-{version}.tar.gz",
            hash="8ffbe944e74043d0d3fb53d4a2a14c94de71f58dbea6a06d0dc92369542958ea",
            dependencies=[
                "ninja",
                "meson",
                "nasm",
            ],
        )

    def build(self):
        Meson.build(self)
        self.install(r"LICENSE share\doc\openh264")
