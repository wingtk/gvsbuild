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
class Luajit(Tarball, Project):
    def __init__(self):
        Project.__init__(
            self,
            "luajit",
            archive_url="http://luajit.org/download/LuaJIT-2.1.0-beta3.tar.gz",
            hash="1ad2e34b111c802f9d0cdf019e986909123237a28c746b21295b63c9e785d9c3",
            patches=["set-paths.patch"],
        )

    def build(self):
        option = "debug" if self.builder.opts.configuration == "debug" else ""
        self.push_location("src")

        self.exec_vs(r".\msvcbuild " + option)

        self.install(
            r".\lua.h .\lualib.h .\luaconf.h .\lauxlib.h .\luajit.h include\luajit-2.1"
        )
        self.install(r".\luajit.exe .\lua51.dll .\lua51.pdb bin")
        self.install(r".\lua51.lib lib")
        self.pop_location()

        self.install(r".\README .\COPYRIGHT share\doc\luajit")
        self.install_pc_files()
