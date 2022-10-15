#  Copyright (C) 2016 - Yevgen Muntyan
#  Copyright (C) 2016 - Ignacio Casal Quinteiro
#  Copyright (C) 2016 - Arnavion
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
class PkgConf(Tarball, Meson):
    def __init__(self):
        Project.__init__(
            self,
            "pkg-config",
            prj_dir="pkgconf",
            archive_url="https://distfiles.dereferenced.org/pkgconf/pkgconf-1.8.0.tar.gz",
            hash="d7b6fdb522d81c11f5a0e0a0629a9f5480809ec90e595058674c1517822dfb8c",
            dependencies=["ninja", "meson"],
            patches=["0001-vs2013.patch"],
        )
        self.add_param("-Dtests=false")

    def build(self):
        Meson.build(self)
        self.install(r".\COPYING share\doc\pkgconf")

    def post_install(self):
        self.exec_cmd(
            r"copy %(gtk_dir)s\bin\pkgconf.exe %(gtk_dir)s\bin\pkg-config.exe"
        )
