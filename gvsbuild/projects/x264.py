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

from gvsbuild.utils.base_expanders import GitRepo
from gvsbuild.utils.base_project import Project, project_add
from gvsbuild.utils.utils import convert_to_msys


@project_add
class X264(GitRepo, Project):
    def __init__(self):
        Project.__init__(
            self,
            "x264",
            repo_url="http://git.videolan.org/git/x264.git",
            fetch_submodules=False,
            dependencies=["nasm", "msys2"],
            tag="31e19f92f00c7003fa115047ce50978bc98c3a0d",
            patches=[
                "x264-0001-Prevent-mb_info_free-to-be-called-before-all-threads.patch",
            ],
        )

    def build(self):
        configuration = (
            "debug-optimized"
            if self.opts.release_configuration_is_actually_debug_optimized
            else self.opts.configuration
        )
        msys_path = Project.get_tool_path("msys2")
        self.exec_vs(
            r"%s\bash build\build.sh %s %s"
            % (
                msys_path,
                convert_to_msys(self.builder.gtk_dir),
                configuration,
            ),
            add_path=msys_path,
        )

        # use the path expected when building with a dependent project
        self.builder.exec_msys(
            ["mv", "libx264.dll.lib", "libx264.lib"],
            working_dir=os.path.join(self.builder.gtk_dir, "lib"),
        )

        if configuration in ["debug-optimized", "debug"]:
            self.install(r".\libx264-164.pdb bin")
            self.install(r".\x264.pdb bin")

        self.install(r".\COPYING share\doc\x264")
