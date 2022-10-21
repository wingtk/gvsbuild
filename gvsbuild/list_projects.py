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
import typer

from gvsbuild.utils.base_project import Project, ProjectType, get_project_by_type


def list_projects(
    project_type: ProjectType = typer.Option(
        None,
        "--type",
        help="Specify type of projects to show, if not selected show all",
        rich_help_panel="Selection Options",
    )
):
    Project.add_all()

    def _list_projects_by_type(project_type):
        projects = get_project_by_type(project_type)
        if projects:
            projects.sort()

            print(f"Available projects with type {project_type}:")
            for project in projects:
                print(f"\t{project[0]:<{Project.name_len}} {project[1]}")

    if project_type:
        _list_projects_by_type(project_type)
    else:
        for project_type in ProjectType:
            _list_projects_by_type(project_type)
