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
from gvsbuild.utils.base_expanders import GitRepo
from gvsbuild.utils.base_project import Project, project_add


@project_add
class Lmdb(GitRepo, Meson):
    def __init__(self):
        Project.__init__(
            self,
            "lmdb",
            repo_url="https://github.com/wingtk/lmdb.git",
            fetch_submodules=False,
            tag="mdb.RE/0.9-meson",
            dependencies=[
                "ninja",
                "meson",
            ],
        )

    def build(self):
        self.push_location(r".\libraries\liblmdb")
        Meson.build(self)
        self.install(r"LICENSE share\doc\lmdb")
        self.pop_location()
