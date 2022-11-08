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
            archive_url="https://download.gnome.org/sources/glib/2.74/glib-2.74.1.tar.xz",
            hash="0ab981618d1db47845e56417b0d7c123f81a3427b2b9c93f5a46ff5bbb964964",
            dependencies=[
                "ninja",
                "meson",
                "pkg-config",
                "gettext",
                "libffi",
                "zlib",
                "pcre2",
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
            archive_url="https://download.gnome.org/sources/glib-networking/2.72/glib-networking-2.72.2.tar.xz",
            hash="cd2a084c7bb91d78e849fb55d40e472f6d8f6862cddc9f12c39149359ba18268",
            dependencies=["pkg-config", "ninja", "meson", "glib", "openssl"],
            patches=[
                "0001-Mark-strings-for-translation-and-translate-just-in-e.patch",
                "0002-tlslog-add-meson-config-setting-to-log-at-debug-leve.patch",
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
