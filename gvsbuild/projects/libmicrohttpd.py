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
class Libmicrohttpd(Tarball, Project):
    def __init__(self):
        Project.__init__(
            self,
            "libmicrohttpd",
            version="1.0.1",
            repository="https://github.com/Karlson2k/libmicrohttpd",
            archive_url="http://ftp.gnu.org/gnu/libmicrohttpd/libmicrohttpd-{version}.tar.gz",
            hash="a89e09fc9b4de34dde19f4fcb4faaa1ce10299b9908db1132bbfa1de47882b94",
            patches=["001-remove-postsample-perf-retries.patch"],
        )

    def build(self):
        if self.builder.opts.configuration == "debug":
            configuration = "debug-dll"
        else:
            configuration = "release-dll"
        td = self.exec_msbuild_gen(
            r"w32", "libmicrohttpd.sln", configuration=configuration
        )
        base_dir = os.path.join("w32", td)

        debug_option = r"_d" if self.builder.opts.configuration == "debug" else ""
        rel_dir = ".\\" + base_dir + r"\Output"
        if not self.builder.x86:
            rel_dir += r"\x64"

        self.push_location(rel_dir)
        self.install(r"microhttpd.h include")
        self.install(f"libmicrohttpd-dll{debug_option}.lib lib")
        self.install(f"libmicrohttpd-dll{debug_option}.dll bin")
        self.install(f"libmicrohttpd-dll{debug_option}.pdb bin")
        self.install(f"hellobrowser-dll{debug_option}.exe bin")
        self.pop_location()

        self.install(r".\COPYING share\doc\libmicrohttpd")
