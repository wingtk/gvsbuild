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

"""
Base tool class, from the project one
"""

import os

from .base_project import Project, GVSBUILD_TOOL

class Tool(Project):
    def __init__(self, name, **kwargs):
        self.dir_part = None
        Project.__init__(self, name, **kwargs)

    def load_defaults(self, builder):
        if self.dir_part:
            self.build_dir = os.path.join(builder.opts.tools_root_dir, self.dir_part)
        else:
            self.build_dir = os.path.join(builder.opts.tools_root_dir, self.name)

    def build(self):
        # All the work is done in the unpack
        pass

    def update_build_dir(self):
        self.unpack()

    def get_path(self):
        # Mandatory for tools
        raise NotImplementedError("get_path")

    @staticmethod
    def add(proj):
        Project.add(proj, type=GVSBUILD_TOOL)

def tool_add(cls):
    """
    Class decorator to add the newly created Toolp class to the global projects/tools/groups list
    """
    Tool.add(cls())
    return cls
