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

import json
import sys
from typing import List

import typer
from packaging import version

from gvsbuild.utils.base_project import Project, ProjectType


def set_projects_latest_versions(projects):
    try:
        import lastversion
    except ImportError:
        print("Please pip install lastversion in your Python environment")
        sys.exit(1)

    projects = {
        project.name: project
        for project in Project.list_projects()
        if project.type.value in [ProjectType.PROJECT, ProjectType.TOOL]
        and not project.internal
    }

    try:
        for project in projects.values():
            if project.internal:
                continue
            project.latest_version = lastversion.latest(
                repo=project.repository or project.name,
                major=project.lastversion_major,
            )
            if project.latest_version:
                project.outdated = version.parse(
                    str(project.latest_version)
                ) > version.parse(project.version)

    except lastversion.utils.ApiCredentialsError:
        print(
            "Create or update the GITHUB token at https://github.com/settings/tokens, then set or update the token environmental variable with:\n$env:GITHUB_API_TOKEN=xxxxxxxxxxxxxxx"
        )
        exit(1)


def list_(
    projects_names: List[str] = typer.Argument(None, help="The projects to list"),
    project_type: ProjectType = typer.Option(
        None,
        "--type",
        help="Specify type of projects to show, if not selected show all",
        rich_help_panel="Selection Options",
    ),
    show_deps: bool = typer.Option(
        False,
        "--deps",
        help="Include dependencies, only useful when selecting the projects to show",
        rich_help_panel="Selection Options",
    ),
    json_: bool = typer.Option(
        False,
        "--json",
        help="Show list in JSON format",
        rich_help_panel="Formatting Options",
    ),
    latest: bool = typer.Option(
        False,
        "--latest",
        help="Fetch latest information",
        rich_help_panel="Formatting Options",
    ),
    outdated: bool = typer.Option(
        False,
        "--outdated",
        help="Only show outdated projects",
        rich_help_panel="Selection Options",
    ),
):
    Project.add_all()

    projects = Project.list_projects()
    if projects_names:
        projects = [project for project in projects if project.name in projects_names]
    if show_deps:
        projects = Project.compute_dependencies(projects)
    if project_type:
        projects = [
            project for project in projects if project.type.value == project_type
        ]

    if outdated:
        latest = True

    if latest:
        set_projects_latest_versions(projects)

    if outdated:
        projects = [
            project
            for project in projects
            if hasattr(project, "outdated") and project.outdated
        ]

    if json_:

        def _get_project_data(project):
            data = {"dependencies": project.dependencies, "type": project.type.value}
            if project.version:
                data["version"] = project.version
            if hasattr(project, "latest_version") and project.latest_version:
                data["latest-version"] = str(project.latest_version)
            return data

        print(
            json.dumps(
                {project.name: _get_project_data(project) for project in projects},
                indent=4,
                sort_keys=True,
            )
        )
    else:
        for project_type in ProjectType:
            type_projects = [
                project for project in projects if project.type == project_type
            ]
            if type_projects:
                print(f"Available projects with type {project_type}:")
                for project in type_projects:
                    params = {
                        "name": f"{project.name:<{Project.name_len}}",
                        "version": f"{project.version:<45}",
                    }
                    if latest:
                        if (
                            hasattr(project, "latest_version")
                            and project.latest_version
                        ):
                            params[
                                "latest_version"
                            ] = f"{str(project.latest_version):<45}"
                        else:
                            params["latest_version"] = "undefined"
                        print("\t{name} {version} {latest_version}".format(**params))
                    else:
                        print("\t{name} {version}".format(**params))
