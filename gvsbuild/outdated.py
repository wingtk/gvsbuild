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

import sys

from packaging import version

from gvsbuild.utils.base_project import Project, ProjectType


def outdated():
    try:
        import lastversion
    except ImportError:
        print("Please pip install lastversion in your Python environment")
        sys.exit(0)

    Project.add_all()
    projects = {
        project.name: project
        for project in Project.list_projects()
        if project.type.value in [ProjectType.PROJECT, ProjectType.TOOL]
        and not project.internal
    }

    print("Looking for projects and tools that are out-of-date, please submit a PR!")
    print(f"\t{'Project Name':<{Project.name_len}} {'Current':<45} {'Latest':<45}")
    try:
        for project in projects.values():
            try:
                latest_version = lastversion.latest(
                    repo=project.repository or project.name,
                    major=project.lastversion_major,
                    even=project.lastversion_even,
                )

                if not latest_version:
                    print(
                        f"\t{project.name:<{Project.name_len}} {project.version:<45} {'No release found':<45}"
                    )
                elif version.parse(str(latest_version)) > version.parse(
                    project.version
                ):
                    print(
                        f"\t{project.name:<{Project.name_len}} {project.version:<45} {str(latest_version):<45}"
                    )
            except version.InvalidVersion:
                print(f"Project {project.name} does not have a valid version")
    except lastversion.exceptions.ApiCredentialsError:
        print(
            "Create or update the GITHUB token at https://github.com/settings/tokens, then set or update the token environmental variable with:\n$env:GITHUB_API_TOKEN=xxxxxxxxxxxxxxx"
        )
