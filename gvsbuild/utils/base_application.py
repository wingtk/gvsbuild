#  Copyright (C) 2016 - Yevgen Muntyan
#  Copyright (C) 2016 - Ignacio Casal Quinteiro
#  Copyright (C) 2016 - Arnavion
#  Copyright (C) 2020 - Daniel F. Dickinson
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
Base application class, from the project one
"""

import os

from .base_project import Project, GVSBUILD_APPLICATION

class Application(Project):
    def __init__(self, name, **kwargs):
        self.dir_part = None
        self.mark_deps = False
        self.application_path = None
        Project.__init__(self, name, **kwargs)

    # def build(self):
        # FIXME: Need to add build machinery for various types of application
        # pass

    def update_build_dir(self):
        self.unpack()

    def get_path(self):
        if self.application_path:
            return self.application_path
        else:
            return self.build_dir

def application_add(cls):
    """
    Class decorator to add the newly created Toolp class to the global projects/tools/groups list
    """
    Project.register(cls, GVSBUILD_APPLICATION)
    return cls
