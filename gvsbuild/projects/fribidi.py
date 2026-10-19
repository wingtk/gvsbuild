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
class Fribidi(Tarball, Meson):
    def __init__(self):
        Project.__init__(
            self,
            "fribidi",
            version="1.0.17",
            repository="https://github.com/fribidi/fribidi",
            archive_url="https://github.com/fribidi/fribidi/releases/download/v{version}/fribidi-{version}.tar.xz",
            hash="6949dcde27d41cebad1fd741fcafc36d55a1020d2d872d4a6eb3914caabbada2",
            dependencies=["ninja", "meson"],
        )

    def build(self):
        Meson.build(self, meson_params=["-Ddocs=false"])
        self.install(r".\COPYING share\doc\fribidi")
