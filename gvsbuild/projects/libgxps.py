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
class Libgxps(Tarball, Meson):
    def __init__(self):
        Project.__init__(
            self,
            "libgxps",
            version="0.3.2",
            archive_url="https://download.gnome.org/sources/libgxps/{major}.{minor}/libgxps-{version}.tar.xz",
            hash="6d27867256a35ccf9b69253eb2a88a32baca3b97d5f4ef7f82e3667fa435251c",
            dependencies=[
                "meson",
                "ninja",
                "pkgconf",
                "glib",
                "libarchive",
                "cairo",
                "libpng",
                "libjpeg-turbo",
                "libtiff-4",
            ],
        )
        if self.opts.enable_gi:
            self.add_dependency("gobject-introspection")
            disable_gi = "false"
        else:
            disable_gi = "true"

        self.add_param(f"-Ddisable-introspection={disable_gi}")
        self.add_param("-Dwith-liblcms2=false")
        self.add_param("-Denable-test=false")

    def build(self):
        Meson.build(self)

        self.install(r".\COPYING share\doc\libgxps")
