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
            archive_url="https://download.gnome.org/sources/glib/2.72/glib-2.72.3.tar.xz",
            hash="4a39a2f624b8512d500d5840173eda7fa85f51c109052eae806acece85d345f0",
            dependencies=["ninja", "meson", "pkg-config", "gettext", "libffi", "zlib"],
            patches=[
                "glib-package-installation-directory.patch",
                "0002-pcre-add-fallback-url.patch",
                "0001-Fix-global-and-local-variables-hidden-by-local-varia.patch",
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
            archive_url="https://download.gnome.org/sources/glib-networking/2.72/glib-networking-2.72.1.tar.xz",
            hash="6fc1bedc8062484dc8a0204965995ef2367c3db5c934058ff1607e5a24d95a74",
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
