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
from gvsbuild.utils.base_expanders import NullExpander, Tarball
from gvsbuild.utils.base_project import Project, project_add


@project_add
class GLib(Tarball, Meson):
    def __init__(self):
        Project.__init__(
            self,
            "glib",
            version="2.78.0",
            lastversion_even=True,
            repository="https://gitlab.gnome.org/GNOME/glib",
            archive_url="https://download.gnome.org/sources/glib/{major}.{minor}/glib-{version}.tar.xz",
            hash="44eaab8b720877ce303c5540b657b126f12dc94972d9880b52959f43fb537b30",
            dependencies=[
                "ninja",
                "meson",
                "pkgconf",
                "gettext",
                "libffi",
                "zlib",
                "pcre2",
            ],
            patches=[
                "glib-package-installation-directory.patch",
            ],
        )

    def build(self):
        Meson.build(self)
        self.install(r".\LICENSES\* share\doc\glib")


@project_add
class GLibNetworking(Tarball, Meson):
    def __init__(self):
        Project.__init__(
            self,
            "glib-networking",
            version="2.78.0",
            lastversion_even=True,
            repository="https://gitlab.gnome.org/GNOME/glib-networking",
            archive_url="https://download.gnome.org/sources/glib-networking/{major}.{minor}/glib-networking-{version}.tar.xz",
            hash="52fe4ce93f7dc51334b102894599858d23c8a65ac4a1110b30920565d68d3aba",
            dependencies=[
                "pkgconf",
                "ninja",
                "meson",
                "glib",
                "openssl",
                "gsettings-desktop-schemas",
            ],
        )

    def build(self):
        Meson.build(
            self, meson_params="-Dgnutls=disabled -Dopenssl=enabled -Dlibproxy=disabled"
        )
        self.install(r".\COPYING share\doc\glib-networking")
        self.install(r".\LICENSE_EXCEPTION share\doc\glib-networking")


@project_add
class GLibPyWrapper(NullExpander, Meson):
    def __init__(self):
        Project.__init__(
            self,
            "glib-py-wrapper",
            dependencies=["glib"],
            version="0.1.0",
            internal=True,
            repository="https://gitlab.gnome.org/GNOME/glib-py-wrapper",
        )

    def build(self):
        Meson.build(self)
