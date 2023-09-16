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

from gvsbuild.utils.base_expanders import Tarball
from gvsbuild.utils.base_project import Project, project_add


@project_add
class Enchant(Tarball, Project):
    def __init__(self):
        Project.__init__(
            self,
            "enchant",
            version="1.6.1",
            archive_url="https://dl.hexchat.net/gtk-win32/src/enchant-{version}.tar.xz",
            hash="d6cddd2621589ca8becaba1bfe8d3668f7d6592743664ef0e1a35543971fbe6e",
            dependencies=["glib"],
        )

    def build(self):
        x64_param = "X64=1" if self.builder.x64 else ""
        self.push_location(r".\src")

        # Exec nmake /nologo -f makefile.mak clean
        self.exec_vs(
            r"nmake /nologo -f makefile.mak DLL=1 "
            + x64_param
            + r" MFLAGS=-MD GLIBDIR=%(gtk_dir)s\include\glib-2.0"
        )

        self.pop_location()

        self.install(
            r".\bin\release\enchant.exe "
            r".\bin\release\pdb\enchant.pdb "
            r".\bin\release\enchant-lsmod.exe "
            r".\bin\release\pdb\enchant-lsmod.pdb "
            r".\bin\release\test-enchant.exe "
            r".\bin\release\pdb\test-enchant.pdb "
            r".\bin\release\libenchant.dll "
            r".\bin\release\pdb\libenchant.pdb "
            r"bin"
        )

        self.install(r".\fonts.conf " r".\fonts.dtd " r"etc\fonts")

        self.install(
            r".\src\enchant.h "
            r".\src\enchant++.h "
            r".\src\enchant-provider.h "
            r"include\enchant"
        )

        self.install(r".\bin\release\libenchant.lib lib")

        self.install(
            r".\bin\release\libenchant_ispell.dll "
            r".\bin\release\libenchant_ispell.lib "
            r".\bin\release\pdb\libenchant_ispell.pdb "
            r".\bin\release\libenchant_myspell.dll "
            r".\bin\release\libenchant_myspell.lib "
            r".\bin\release\pdb\libenchant_myspell.pdb "
            r"lib\enchant"
        )

        self.install(r".\COPYING.LIB share\doc\enchant")
