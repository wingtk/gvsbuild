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

import os

from gvsbuild.utils.base_expanders import Tarball
from gvsbuild.utils.base_project import Project, project_add


@project_add
class AdwaitaIconTheme(Tarball, Project):
    def __init__(self):
        Project.__init__(
            self,
            "adwaita-icon-theme",
            archive_url="https://download.gnome.org/sources/adwaita-icon-theme/40/adwaita-icon-theme-40.1.1.tar.xz",
            hash="0b6c436ed6ad9887a88ada1f72a0197b1eb73b020d8d344abab4c7fa7250f8f6",
            dependencies=[
                "librsvg",
                "python",
            ],
        )

    def build(self):
        # Create the destination dir, before the build
        os.makedirs(
            os.path.join(self.builder.gtk_dir, "share", "icons", "Adwaita"),
            exist_ok=True,
        )

        self.push_location(r".\win32")
        self.exec_vs(
            r'nmake /nologo /f adwaita-msvc.mak CFG=%(configuration)s PYTHON="%(python_dir)s\python.exe" PREFIX="%(gtk_dir)s"',
            add_path=os.path.join(self.builder.opts.msys_dir, "usr", "bin"),
        )
        self.exec_vs(
            r'nmake /nologo /f adwaita-msvc.mak install CFG=%(configuration)s PYTHON="%(python_dir)s\python.exe" PREFIX="%(gtk_dir)s"',
            add_path=os.path.join(self.builder.opts.msys_dir, "usr", "bin"),
        )
        self.pop_location()

        self.install(r".\COPYING_CCBYSA3 share\doc\adwaita-icon-theme")
