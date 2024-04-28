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
class Cairo(Tarball, Meson):
    def __init__(self):
        Meson.__init__(
            self,
            "cairo",
            version="1.18.0",
            lastversion_even=True,
            archive_url="https://gitlab.freedesktop.org/cairo/cairo/-/archive/{version}/cairo-{version}.tar.gz",
            hash="39a78afdc33a435c0f2ab53a5ec2a693c3c9b6d2ec9783ceecb2b94d54d942b0",
            dependencies=["freetype", "glib", "pixman", "libpng"],
            patches=["0001-fix-alloca-unresolved.patch"],
        )
        self.add_param("-Ddwrite=enabled")
        self.add_param("-Dfreetype=enabled")
        self.add_param("-Dfontconfig=disabled")

    def build(self):
        Meson.build(self)
        self.install(r".\COPYING share\doc\cairo")
