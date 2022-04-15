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

from gvsbuild.utils.base_builders import Meson
from gvsbuild.utils.base_expanders import Tarball
from gvsbuild.utils.base_project import Project, project_add


@project_add
class Fontconfig(Tarball, Meson):
    def __init__(self):
        Project.__init__(
            self,
            "fontconfig",
            archive_url="https://www.freedesktop.org/software/fontconfig/release/fontconfig-2.14.0.tar.gz",
            hash="b8f607d556e8257da2f3616b4d704be30fd73bd71e367355ca78963f9a7f0434",
            dependencies=["freetype", "libxml2"],
        )

    def build(self):
        Meson.build(self)
        self.install(r".\COPYING share\doc\fontconfig")
