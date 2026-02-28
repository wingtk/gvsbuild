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
class Libsoup2(Tarball, Meson):
    def __init__(self):
        Project.__init__(
            self,
            "libsoup2",
            lastversion_major=2,
            repository="https://gitlab.gnome.org/GNOME/libsoup",
            version="2.74.3",
            lastversion_even=True,
            archive_url="https://download.gnome.org/sources/libsoup/{major}.{minor}/libsoup-{version}.tar.xz",
            hash="e4b77c41cfc4c8c5a035fcdc320c7bc6cfb75ef7c5a034153df1413fa1d92f13",
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
        enable_gi = "enabled" if self.opts.enable_gi else "disabled"
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
            version="3.6.6",
            lastversion_major=3,
            lastversion_even=True,
            repository="https://gitlab.gnome.org/GNOME/libsoup",
            archive_url="https://download.gnome.org/sources/libsoup/{major}.{minor}/libsoup-{version}.tar.xz",
            hash="51ed0ae06f9d5a40f401ff459e2e5f652f9a510b7730e1359ee66d14d4872740",
            dependencies=[
                "libxml2",
                "glib-networking",
                "sqlite",
                "libpsl",
                "mit-kerberos",
                "nghttp2",
            ],
        )

        if self.opts.enable_gi:
            self.add_dependency("gobject-introspection")
        enable_gi = "enabled" if self.opts.enable_gi else "disabled"
        self.add_param(f"-Dintrospection={enable_gi}")
        self.add_param("-Dvapi=disabled")
        self.add_param("-Dsysprof=disabled")
        self.add_param("-Dtls_check=false")
        self.add_param("-Dtests=false")

    def build(self):
        Meson.build(self)

        self.install(r".\COPYING share\doc\libsoup3")
