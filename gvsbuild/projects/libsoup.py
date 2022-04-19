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
class Libsoup2(Tarball, Meson):
    def __init__(self):
        Project.__init__(
            self,
            "libsoup2",
            archive_url="https://download.gnome.org/sources/libsoup/2.74/libsoup-2.74.2.tar.xz",
            hash="f0a427656e5fe19e1df71c107e88dfa1b2e673c25c547b7823b6018b40d01159",
            dependencies=[
                "libxml2",
                "glib-networking",
                "sqlite",
                "libpsl",
                "mit-kerberos",
            ],
        )

        if self.opts.enable_gi:
            self.add_dependency("gobject-introspection")
            enable_gi = "enabled"
        else:
            enable_gi = "disabled"

        self.add_param(f"-Dintrospection={enable_gi}")
        self.add_param("-Dvapi=disabled")
        self.add_param("-Dsysprof=disabled")
        self.add_param("-Dtls_check=false")
        self.add_param("-Dtests=false")

    def build(self):
        Meson.build(self)

        self.install(r".\COPYING share\doc\libsoup2")


@project_add
class Libsoup3(Tarball, Meson):
    def __init__(self):
        Project.__init__(
            self,
            "libsoup3",
            archive_url="https://download.gnome.org/sources/libsoup/3.0/libsoup-3.0.6.tar.xz",
            hash="b45d59f840b9acf9bb45fd45854e3ef672f57e3ab957401c3ad8d7502ac23da6",
            dependencies=[
                "libxml2",
                "glib-networking",
                "sqlite",
                "libpsl",
                "mit-kerberos",
                "nghttp2",
            ],
            patches=[
                "0001-server-message-proxy-the-peer-certificate-and-peer-c.patch",
            ],
        )

        if self.opts.enable_gi:
            self.add_dependency("gobject-introspection")
            enable_gi = "enabled"
        else:
            enable_gi = "disabled"

        self.add_param(f"-Dintrospection={enable_gi}")
        self.add_param("-Dvapi=disabled")
        self.add_param("-Dsysprof=disabled")
        self.add_param("-Dtls_check=false")
        self.add_param("-Dtests=false")

    def build(self):
        Meson.build(self)

        self.install(r".\COPYING share\doc\libsoup3")
