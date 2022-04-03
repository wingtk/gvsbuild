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
class SQLite(Tarball, Project):
    def __init__(self):
        Project.__init__(
            self,
            "sqlite",
            archive_url="https://www.sqlite.org/2020/sqlite-autoconf-3310100.tar.gz",
            hash="62284efebc05a76f909c580ffa5c008a7d22a1287285d68b7825a2b6b51949ae",
        )

    def build(self):
        nmake_debug = (
            "DEBUG=2" if self.builder.opts.configuration == "debug" else "DEBUG=0"
        )
        self.exec_vs(f"nmake /f Makefile.msc sqlite3.dll DYNAMIC_SHELL=1 {nmake_debug}")

        self.install("sqlite3.h include")
        self.install("sqlite3ext.h include")
        self.install("sqlite3.dll sqlite3.pdb bin")
        self.install("sqlite3.lib lib")
