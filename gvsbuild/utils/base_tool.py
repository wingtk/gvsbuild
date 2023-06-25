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

"""Base tool class, from the project one."""

import os

from .base_project import Project, ProjectType


class Tool(Project):
    def __init__(self, name, **kwargs):
        self.dir_part = None
        self.mark_deps = False
        self.tool_path = None
        self.full_exe = None
        Project.__init__(self, name, **kwargs)

        if self.dir_part:
            self.dir_part = (self.dir_part).format(**self.version_params)

    def load_defaults(self):
        if self.dir_part:
            self.build_dir = os.path.join(self.opts.tools_root_dir, self.dir_part)
        else:
            self.build_dir = os.path.join(self.opts.tools_root_dir, self.name)
        if hasattr(self, "exe_name"):
            self.full_exe = os.path.join(self.build_dir, self.exe_name)

    def tool_mark(self):
        # Create the directory to let the --fast-build option work as expected
        if not os.path.exists(self.build_dir):
            os.makedirs(self.build_dir)
            self.mark_deps = True

    def build(self):
        # All the work is done in the unpack & we don't force the rebuild of all projects that uses this tool
        return not self.mark_deps

    def update_build_dir(self):
        self.unpack()

    def get_path(self):
        return self.tool_path or self.build_dir

    def get_executable(self):
        if self.full_exe:
            return self.full_exe
        raise NotImplementedError(f"{self.name}:get_executable")

    def get_base_dir(self):
        """Base directory for the tool, used for perl to have the dir to pass
        to the *make tool, normally not used (we update the path or use
        directly the executable)"""
        raise NotImplementedError("get_base_dir")

    def export(self):
        # We do not want to export tools
        pass


def tool_add(cls):
    """Class decorator to add the newly created Toolp class to the global
    projects/tools/groups list."""
    Project.register(cls, ProjectType.TOOL)
    return cls
