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

from gvsbuild.utils.base_expanders import Tarball
from gvsbuild.utils.base_project import Project, project_add


@project_add
class Gettext(Tarball, Project):
    def __init__(self):
        Project.__init__(
            self,
            "gettext",
            archive_url="http://ftp.gnu.org/pub/gnu/gettext/gettext-0.19.7.tar.gz",
            hash="5386d2a40500295783c6a52121adcf42a25519e2d23675950619c9e69558c23f",
            dependencies=["win-iconv"],
            patches=[
                "0001-gettext-runtime-Add-pre-configured-headers-for-MSVC-.patch",
                "0001-gettext-tools-Add-pre-configured-headers-and-sources.patch",
                "0001-gettext-tools-gnulib-lib-libxml-Check-for-_WIN32-as-.patch",
                "0001-gettext-tools-Make-private-headers-C-friendly.patch",
                "0001-gettext-tools-src-x-lua.c-Fix-C99ism.patch",
                "0002-gettext-tools-gnulib-lib-Declare-items-at-top-of-blo.patch",
                "0004-gettext-runtime-intl-plural-exp.h-Match-up-declarati.patch",
                "0005-gettext-runtime-intl-printf-parse.c-Fix-build-on-Vis.patch",
                "0006-gettext-intrinsics.patch",
            ],
        )

    def build(self):
        self.exec_msbuild_gen(r"build\win32", "gettext.sln")

        self.install(r".\gettext-tools\its\*.its share\gettext\its")
        self.install(r".\gettext-tools\its\*.loc share\gettext\its")
        self.install(r".\COPYING share\doc\gettext")
