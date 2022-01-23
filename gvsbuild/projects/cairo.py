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
class Cairo(Tarball, Project):
    def __init__(self):
        Project.__init__(
            self,
            "cairo",
            archive_url="https://cairographics.org/releases/cairo-1.16.0.tar.xz",
            hash="5e7b29b3f113ef870d1e3ecf8adf21f923396401604bda16d44be45e66052331",
            dependencies=["fontconfig", "glib", "pixman", "libpng"],
            patches=["0001-Fix-mask-usage-in-image-compositor.patch"],
        )

    def build(self):
        self.exec_vs(
            r"make -f Makefile.win32 CFG=%(configuration)s ARCH=%(platform)s",
            add_path=os.path.join(self.builder.opts.msys_dir, "usr", "bin"),
        )
        self.push_location(r".\util\cairo-gobject")
        self.exec_vs(
            r"make -f Makefile.win32 CFG=%(configuration)s ARCH=%(platform)s",
            add_path=os.path.join(self.builder.opts.msys_dir, "usr", "bin"),
        )
        self.pop_location()

        self.install(r".\src\%(configuration)s\cairo.dll bin")
        self.install(r".\util\cairo-gobject\%(configuration)s\cairo-gobject.dll bin")

        self.install(r".\src\%(configuration)s\cairo.lib lib")
        self.install(r".\util\cairo-gobject\%(configuration)s\cairo-gobject.lib lib")

        self.install(r".\src\cairo.h include\cairo")
        self.install(r".\src\cairo-deprecated.h include\cairo")
        self.install(r".\src\cairo-pdf.h include\cairo")
        self.install(r".\src\cairo-ps.h include\cairo")
        self.install(r".\src\cairo-script.h include\cairo")
        self.install(r".\src\cairo-svg.h include\cairo")
        self.install(r".\src\cairo-tee.h include\cairo")
        self.install(r".\src\cairo-win32.h include\cairo")
        self.install(r".\src\cairo-xml.h include\cairo")
        self.install(r".\src\cairo-ft.h include\cairo")
        self.install(r".\src\cairo-features.h include\cairo")
        self.install(r".\util\cairo-gobject\cairo-gobject.h include\cairo")
        self.install(r".\cairo-version.h include\cairo")

        self.install_pc_files()
        self.install(r".\COPYING share\doc\cairo")
