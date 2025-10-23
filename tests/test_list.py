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

import gvsbuild.groups  # noqa: F401
import gvsbuild.projects  # noqa: F401
import gvsbuild.tools  # noqa: F401
from gvsbuild.utils.base_project import Project, ProjectType


def test_list(app, runner):
    Project.add_all()
    projects = Project.list_projects()

    result = runner.invoke(app, ["list"])
    assert result.exit_code == 0
    for project_type in [ProjectType.GROUP, ProjectType.PROJECT, ProjectType.TOOL]:
        for project_name in [
            project.name for project in projects if project.type == project_type
        ]:
            assert project_name in result.stdout
