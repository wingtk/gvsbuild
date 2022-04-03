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
class Libsoup(Tarball, Meson):
    def __init__(self):
        Project.__init__(
            self,
            "libsoup",
            archive_url="https://download.gnome.org/sources/libsoup/2.72/libsoup-2.72.0.tar.xz",
            hash="170c3f8446b0f65f8e4b93603349172b1085fb8917c181d10962f02bb85f5387",
            dependencies=[
                "libxml2",
                "glib-networking",
                "sqlite",
                "libpsl",
                "mit-kerberos",
            ],
            patches=["0001-Improve-support-for-rfc-7230.patch"],
        )

        if self.opts.enable_gi:
            self.add_dependency("gobject-introspection")
            enable_gi = "enabled"
        else:
            enable_gi = "disabled"

        self.add_param("-Dintrospection={}".format(enable_gi))
        self.add_param("-Dvapi=disabled")
        self.add_param("-Dsysprof=disabled")
        self.add_param("-Dtls_check=false")
        self.add_param("-Dtests=false")

    def build(self):
        Meson.build(self)

        self.install(r".\COPYING share\doc\libsoup")


@project_add
class Libsoup3(Tarball, Meson):
    def __init__(self):
        Project.__init__(
            self,
            "libsoup3",
            archive_url="https://download.gnome.org/sources/libsoup/3.0/libsoup-3.0.5.tar.xz",
            hash="f5d143db6830b3825edc2a1c4449d639273b0bfa017a4970871962d9bca22145",
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

        self.add_param("-Dintrospection={}".format(enable_gi))
        self.add_param("-Dvapi=disabled")
        self.add_param("-Dsysprof=disabled")
        self.add_param("-Dtls_check=false")
        self.add_param("-Dtests=false")

    def build(self):
        Meson.build(self)

        self.install(r".\COPYING share\doc\libsoup3")
