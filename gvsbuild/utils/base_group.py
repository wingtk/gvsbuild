#  Copyright (C) 2016 - Yevgen Muntyan
#  Copyright (C) 2016 - Ignacio Casal Quinteiro
#  Copyright (C) 2016 - Arnavion
#  Copyright (C) 2017 - Daniele Forghieri
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
Base group class, from the project one, as a placeholder to build more than
one project from a single one
"""

from .base_project import Project, GVSBUILD_GROUP

class Group(Project):
    def __init__(self, name, **kwargs):
        Project.__init__(self, name, **kwargs)

    def unpack(self):
        # We don't have to do anything
        pass

    def build(self):
        pass

    @staticmethod
    def add(proj):
        Project.add(proj, type=GVSBUILD_GROUP)
