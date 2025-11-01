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

import os

from gvsbuild.utils.base_builders import Meson
from gvsbuild.utils.base_expanders import Tarball
from gvsbuild.utils.base_project import project_add


@project_add
class AdwaitaIconTheme(Tarball, Meson):
    def __init__(self):
        Meson.__init__(
            self,
            "adwaita-icon-theme",
            version="49.0",
            repository="https://gitlab.gnome.org/GNOME/adwaita-icon-theme",
            archive_url="https://download.gnome.org/sources/adwaita-icon-theme/{major}/adwaita-icon-theme-{version}.tar.xz",
            hash="65166461d1b278aa942f59aa8d0fccf1108d71c65f372c6266e172449791755c",
            dependencies=[
                "hicolor-icon-theme",
                "librsvg",
                "gtk4",
            ],
        )

    def build(self):
        Meson.build(self)
        # Work around for https://gitlab.gnome.org/GNOME/adwaita-icon-theme/-/issues/282
        self.builder.exec_msys(
            [
                "cp",
                "--remove-destination",
                "places/folder.svg",
                "status/folder-open.svg",
            ],
            working_dir=os.path.join(
                self.builder.gtk_dir, "share", "icons", "Adwaita", "scalable"
            ),
        )
        self.install(r".\COPYING_CCBYSA3 share\doc\adwaita-icon-theme")
