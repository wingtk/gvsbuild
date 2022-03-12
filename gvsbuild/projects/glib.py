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
from gvsbuild.utils.base_expanders import NullExpander, Tarball
from gvsbuild.utils.base_project import Project, project_add


@project_add
class GLib(Tarball, Meson):
    def __init__(self):
        Project.__init__(
            self,
            "glib",
            archive_url="https://download.gnome.org/sources/glib/2.70/glib-2.70.3.tar.xz",
            hash="233fa4841c1e19e396db7607d58f6b75ba3313c50bf0fce07b2e3532d5eb7d46",
            dependencies=["ninja", "meson", "pkg-config", "gettext", "libffi", "zlib"],
            patches=[
                "glib-package-installation-directory.patch",
                "0001-_g_stat_size-return-goffset.patch",
                "0002-pcre-add-fallback-url.patch",
            ],
        )

    def build(self):
        Meson.build(self)
        self.install(r".\COPYING share\doc\glib")


@project_add
class GLibNetworking(Tarball, Meson):
    def __init__(self):
        Project.__init__(
            self,
            "glib-networking",
            archive_url="https://ftp.acc.umu.se/pub/gnome/sources/glib-networking/2.70/glib-networking-2.70.0.tar.xz",
            hash="66b408e7afa86c582fe38963db56133869ab4b57d34e48ec56aba621940d6f35",
            dependencies=["pkg-config", "ninja", "meson", "glib", "openssl"],
            patches=[
                "0001-Do-not-load-certificates-from-default-paths-on-MacOS.patch",
                "0002-Loading-certificates-from-Windows-root-and-ca-stores.patch",
            ],
        )

    def build(self):
        Meson.build(self, meson_params="-Dgnutls=disabled -Dopenssl=enabled")
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
        )

    def build(self):
        Meson.build(self)
