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
from gvsbuild.utils.base_project import project_add


@project_add
class Graphene(Tarball, Meson):
    def __init__(self):
        Meson.__init__(
            self,
            "graphene",
            version="1.10.8",
            repository="ebassi/graphene",
            archive_url="https://github.com/ebassi/graphene/archive/refs/tags/{version}.tar.gz",
            archive_filename="graphene-{version}.tar.gz",
            hash="922dc109d2dc5dc56617a29bd716c79dd84db31721a8493a13a5f79109a4a4ed",
            dependencies=["ninja", "meson", "pkgconf", "glib"],
            patches=["001-fix-python-lookup.patch"],
        )
        if self.opts.enable_gi:
            self.add_dependency("gobject-introspection")
            enable_gi = "enabled"
        else:
            enable_gi = "disabled"

        self.add_param(f"-Dintrospection={enable_gi}")

    def build(self):
        Meson.build(self, make_tests=True)
        self.install(r".\LICENSE share\doc\graphene")
