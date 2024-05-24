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

from gvsbuild.utils.base_expanders import Tarball
from gvsbuild.utils.base_project import Project, project_add


@project_add
class HicolorIconTheme(Tarball, Project):
    def __init__(self):
        Project.__init__(
            self,
            "hicolor-icon-theme",
            version="0.18",
            repository="https://gitlab.freedesktop.org/xdg/default-icon-theme",
            archive_url="http://icon-theme.freedesktop.org/releases/hicolor-icon-theme-{version}.tar.xz",
            hash="db0e50a80aa3bf64bb45cbca5cf9f75efd9348cf2ac690b907435238c3cf81d7",
        )

    def build(self):
        self.install(r".\index.theme share\icons\hicolor")
