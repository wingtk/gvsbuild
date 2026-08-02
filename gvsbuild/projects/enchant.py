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

from pathlib import Path

from gvsbuild.utils.base_expanders import Tarball
from gvsbuild.utils.base_project import Project, project_add


@project_add
class Enchant(Tarball, Project):
    def __init__(self):
        Project.__init__(
            self,
            "enchant",
            version="2.8.19",
            repository="https://github.com/rrthomas/enchant",
            archive_url="https://github.com/rrthomas/enchant/releases/download/v{version}/enchant-{version}.tar.gz",
            hash="c8d70991d544ee39274b96bd01d2858a009fe732ff43f2aaf605fd61ecd06f60",
            dependencies=["glib"],
        )

    def build(self):
        self.push_location(r".\src")
        cmd = [
            "nmake",
            "/nologo",
            "-f",
            "makefile.mak",
            "DLL=1",
            "MFLAGS=-MD",
            f"GLIBDIR={Path(self.builder.gtk_dir) / 'include' / 'glib-2.0'}",
        ]
        if self.builder.x64:
            cmd.append("X64=1")
        self.exec_vs(cmd)

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
            r".\lib\enchant.h "
            r".\lib\enchant++.h "
            r".\lib\enchant-provider.h "
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
