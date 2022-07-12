#  Copyright (C) 2016 - Yevgen Muntyan
#  Copyright (C) 2016 - Ignacio Casal Quinteiro
#  Copyright (C) 2016 - Arnavion
#  Copyright (C) 2022 - Nefo Fortressia
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
class Libadwaita(Tarball, Meson):
    def __init__(self):
        Project.__init__(
            self,
            "libadwaita",
            archive_url="https://download.gnome.org/sources/libadwaita/1.1/libadwaita-1.1.2.tar.xz",
            hash="2b5ca4104c21a36e31f900ef117ab887dd9d471f6a65d2ba374ce0339314219f",
            dependencies=[
                "ninja",
                "meson",
                "pkg-config",
                "glib",
                "gtk4",
            ],
        )
        gir = "disabled"
        if self.opts.enable_gi:
            self.add_dependency("gobject-introspection")
            gir = "enabled"

        self.add_param(f"-Dintrospection={gir}")
        self.add_param("-Dgtk_doc=false")
        self.add_param("-Dvapi=false")

    def build(self, **kwargs):
        Meson.build(self, make_tests=True)
        self.install(r".\COPYING share\doc\libadwaita")
