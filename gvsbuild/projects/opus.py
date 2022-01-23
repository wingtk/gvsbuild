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
class Opus(Tarball, Project):
    def __init__(self):
        Project.__init__(
            self,
            "opus",
            archive_url="https://archive.mozilla.org/pub/opus/opus-1.3.1.tar.gz",
            hash="65b58e1e25b2a114157014736a3d9dfeaad8d41be1c8179866f144a2fb44ff9d",
        )

    def build(self):
        configuration = "ReleaseDLL"
        if self.builder.opts.configuration == "debug":
            configuration = "DebugDLL"

        td = self.exec_msbuild_gen(r".\win32", "opus.sln", configuration=configuration)
        bin_dir = os.path.join(
            r".\win32", td, self.builder.opts.platform, configuration
        )

        self.install(bin_dir + r"\opus.dll bin")
        self.install(bin_dir + r"\opus.pdb bin")

        self.install(bin_dir + r"\opus.lib lib")

        self.install(r"include\* include")

        self.install_pc_files()

        self.install(r"COPYING share\doc\opus")
