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

import os

from gvsbuild.utils.base_expanders import Tarball
from gvsbuild.utils.base_project import Project, project_add


@project_add
class Gettext(Tarball, Project):
    def __init__(self):
        Project.__init__(
            self,
            "gettext",
            version="0.21",
            repository="autotools-mirror/gettext",
            archive_url="http://ftp.gnu.org/pub/gnu/gettext/gettext-{version}.tar.xz",
            hash="d20fcbb537e02dcf1383197ba05bd0734ef7bf5db06bdb241eb69b7d16b73192",
            dependencies=["win-iconv"],
            patches=[
                "gettext-runtime-c99.patch",
                "gettext-tools-c99.patch",
                "gettext-tools-gnulib-memset.patch",
                "libtextstyle-c99.patch",
            ],
        )

    def build(self):
        self.push_location(r".\nmake")
        self.exec_vs(
            r'nmake /nologo /f Makefile.vc CFG=%(configuration)s PYTHON="%(python_dir)s\python.exe" PREFIX="%(gtk_dir)s"',
            add_path=os.path.join(self.builder.opts.msys_dir, "usr", "bin"),
        )
        self.pop_location()

        self.push_location(
            r".\nmake\vs%s\%s\%s"
            % (
                self.builder.opts.vs_ver,
                self.builder.opts.configuration,
                self.builder.opts.platform,
            )
        )
        self.install(r".\asprintf.dll bin")
        self.install(r".\asprintf.pdb bin")
        self.install(r".\intl.dll bin")
        self.install(r".\intl.pdb bin")
        self.install(r".\envsubst.exe bin")
        self.install(r".\envsubst.pdb bin")
        self.install(r".\gettext.exe bin")
        self.install(r".\gettext.pdb bin")
        self.install(r".\ngettext.exe bin")
        self.install(r".\ngettext.pdb bin")
        self.install(r".\gettextpo.dll bin")
        self.install(r".\gettextpo.pdb bin")
        self.install(r".\gettextlib-*.dll bin")
        self.install(r".\gettextlib-*.pdb bin")
        self.install(r".\gettextsrc-*.dll bin")
        self.install(r".\gettextsrc-*.pdb bin")
        self.install(r".\msg*.exe bin")
        self.install(r".\msg*.pdb bin")
        self.install(r".\xgettext.exe bin")
        self.install(r".\xgettext.pdb bin")
        self.install(r".\recode-sr-latin.exe bin")
        self.install(r".\recode-sr-latin.pdb bin")
        self.install(r".\textstyle.dll bin")
        self.install(r".\textstyle.pdb bin")

        self.install(r".\asprintf.lib lib")
        self.install(r".\intl.lib lib")
        self.install(r".\gettextpo.lib lib")
        self.pop_location()

        self.push_location(r".\msvc")
        self.install(r".\gettext-runtime\libasprintf\autosprintf.h include")
        self.install(r".\gettext-runtime\intl\libgnuintl.h include")
        self.install(r".\gettext-tools\libgettextpo\gettext-po.h include")
        self.pop_location()

        self.install(r".\gettext-tools\its\*.its share\gettext\its")
        self.install(r".\gettext-tools\its\*.loc share\gettext\its")
        self.install(r".\COPYING share\doc\gettext")

    def post_install(self):
        self.builder.exec_msys(
            ["mv", "libgnuintl.h", "libintl.h"],
            working_dir=os.path.join(self.builder.gtk_dir, "include"),
        )
