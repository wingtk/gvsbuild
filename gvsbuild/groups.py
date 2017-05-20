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
Default groups of projects
"""

from .utils.base_group import Group
from .utils.base_project import Project, GVSBUILD_PROJECT

class Group_Tools(Group):
    def __init__(self):
        Group.__init__(self,
            'tools',
            dependencies = [
                'cmake',
                'meson',
                'nasm',
                'ninja',
                'nuget',
                'perl',
                'python',
                'yasm',
                ],
            )

Group.add(Group_Tools())

class Group_Gtk3_Full(Group):
    def __init__(self):
        Group.__init__(self,
            'gtk3-full',
            dependencies = [
                'adwaita-icon-theme',
                'clutter',
                'emeus',
                'gtk3',
                'gtksourceview3',
                'hicolor-icon-theme',
                'pkg-config',
                'wing',
                ],
            )

Group.add(Group_Gtk3_Full())

class Group_All(Group):
    def __init__(self):
        all_prj = [x.name for x in Project._projects if x.type == GVSBUILD_PROJECT]
        Group.__init__(self,
            'all',
            dependencies = all_prj
        )

Group.add(Group_All())
