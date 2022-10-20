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
import sys

from gvsbuild.utils.base_project import Project, ProjectType, get_project_by_type


def do_list_type(prj_type, desc):
    projects = get_project_by_type(prj_type)
    if projects:
        projects.sort()

        print(f"{desc}:")
        for project in projects:
            print(f"\t{project[0]:<{Project.name_len}} {project[1]}")


def list_projects():
    Project.add_all()
    do_list_type(ProjectType.TOOL, "Available tools")
    do_list_type(ProjectType.PROJECT, "Available projects")
    do_list_type(ProjectType.GROUP, "Available groups")
    do_list_type(ProjectType.IGNORE, "Developer project(s)")
    sys.exit(0)
