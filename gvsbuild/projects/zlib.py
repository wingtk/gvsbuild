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
class Zlib(Tarball, Project):
    def __init__(self):
        Project.__init__(
            self,
            "zlib",
            archive_url="http://www.zlib.net/zlib-1.2.12.tar.xz",
            hash="7db46b8d7726232a621befaab4a1c870f00a90805511c0e0090441dac57def18",
        )

    def build(self):
        options = ""
        if self.builder.opts.configuration == "debug":
            options = 'CFLAGS="-nologo -MDd -W3 -Od -Zi -Fd\\"zlib\\""'

        self.exec_vs(
            r"nmake /nologo /f win32\Makefile.msc STATICLIB=zlib-static.lib IMPLIB=zlib1.lib "
            + options
        )

        self.install(r".\zlib.h .\zconf.h include")
        self.install(r".\zlib1.dll .\zlib1.pdb bin")
        self.install(r".\zlib1.lib lib")

        self.install_pc_files()
        self.install(r".\README share\doc\zlib")
