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

from gvsbuild.utils.base_builders import Meson
from gvsbuild.utils.base_expanders import Tarball
from gvsbuild.utils.base_project import Project, project_add


@project_add
class Libadwaita(Tarball, Meson):
    def __init__(self):
        Project.__init__(
            self,
            "libadwaita",
            repository="https://gitlab.gnome.org/GNOME/libadwaita",
            version="1.7.2",
            archive_url="https://download.gnome.org/sources/libadwaita/{major}.{minor}/libadwaita-{version}.tar.xz",
            hash="28ee2ff589c6debe47af9da7a56e37c97d6849e003918a4b223f690d25f960be",
            dependencies=[
                "ninja",
                "meson",
                "msys2",
                "pkgconf",
                "glib",
                "gtk4",
            ],
            patches=[
                "0001-remove-appstream-dependency.patch",
            ],
        )
        gir = "disabled"
        if self.opts.enable_gi:
            self.add_dependency("gobject-introspection")
            gir = "enabled"

        self.add_param(f"-Dintrospection={gir}")
        self.add_param("-Dgtk_doc=false")
        self.add_param("-Dvapi=false")
        # https://gitlab.gnome.org/GNOME/libadwaita/-/issues/931
        self.add_param("-Dtests=false")

    def build(self, **kwargs):
        Meson.build(self)
        self.install(r".\COPYING share\doc\libadwaita")
