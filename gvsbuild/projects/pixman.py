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

import os

from gvsbuild.utils.base_expanders import Tarball
from gvsbuild.utils.base_project import Project, project_add


@project_add
class Pixman(Tarball, Project):
    def __init__(self):
        Project.__init__(
            self,
            "pixman",
            repository="https://gitlab.freedesktop.org/pixman/pixman",
            version="0.42.2",
            lastversion_even=True,
            archive_url="http://cairographics.org/releases/pixman-{version}.tar.gz",
            hash="ea1480efada2fd948bc75366f7c349e1c96d3297d09a3fe62626e38e234a625e",
        )

    def build(self):
        optimizations = "SSE2=on SSSE3=on" + (
            " MMX=off" if self.builder.x64 else " MMX=on"
        )

        add_path = os.path.join(self.builder.opts.msys_dir, "usr", "bin")

        self.exec_vs(
            f"make -f Makefile.win32 pixman CFG=%(configuration)s {optimizations}",
            add_path=add_path,
        )

        self.install(r".\pixman\%(configuration)s\pixman-1.lib lib")

        self.install(r".\pixman\pixman.h include\pixman-1")
        self.install(r".\pixman\pixman-version.h include\pixman-1")

        self.install(r".\COPYING share\doc\pixman")
