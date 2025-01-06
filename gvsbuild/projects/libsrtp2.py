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
class LibSRTP(Tarball, Meson):
    def __init__(self):
        Project.__init__(
            self,
            "libsrtp2",
            repository="https://github.com/cisco/libsrtp",
            version="2.5.0",
            archive_url="https://github.com/cisco/libsrtp/archive/refs/tags/v{version}.tar.gz",
            hash="8a43ef8e9ae2b665292591af62aa1a4ae41e468b6d98d8258f91478735da4e09",
            dependencies=["meson", "ninja"],
        )

    def build(self):
        Meson.build(self)
        self.install(r".\LICENSE share\doc\libsrtp2")
