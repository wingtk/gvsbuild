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

from gvsbuild.utils.base_expanders import GitRepo
from gvsbuild.utils.base_project import Project, project_add


@project_add
class Luajit(GitRepo, Project):
    def __init__(self):
        Project.__init__(
            self,
            "luajit",
            version="2.1.1692716794",
            repo_url="https://github.com/LuaJIT/LuaJIT",
            fetch_submodules=False,
            tag="03c31124cc3b521ef54fe398e10fa55660a5057d",
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
