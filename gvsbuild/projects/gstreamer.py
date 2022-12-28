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

import os

from gvsbuild.utils.base_builders import Meson
from gvsbuild.utils.base_expanders import Tarball
from gvsbuild.utils.base_project import Project, project_add


@project_add
class GStreamer(Tarball, Meson):
    def __init__(self):
        Project.__init__(
            self,
            "gstreamer",
            repository="https://gitlab.freedesktop.org/gstreamer/gstreamer",
            version="1.20.5",
            archive_url="https://gstreamer.freedesktop.org/src/gstreamer/gstreamer-{version}.tar.xz",
            hash="5a19083faaf361d21fc391124f78ba6d609be55845a82fa8f658230e5fa03dff",
            dependencies=["meson", "ninja", "glib", "orc"],
        )

        if self.opts.enable_gi:
            self.add_dependency("gobject-introspection")
            enable_gi = "enabled"
        else:
            enable_gi = "disabled"

        self.add_param(f"-Dintrospection={enable_gi}")

    def build(self):
        add_path = os.path.join(self.builder.opts.msys_dir, "usr", "bin")

        Meson.build(
            self, add_path=add_path, meson_params="-Dtests=disabled -Dexamples=disabled"
        )
        self.install(r".\COPYING share\doc\gstreamer")


@project_add
class Orc(Tarball, Meson):
    def __init__(self):
        Project.__init__(
            self,
            "orc",
            version="0.4.33",
            repository="https://gitlab.freedesktop.org/gstreamer/orc",
            archive_url="https://gstreamer.freedesktop.org/src/orc/orc-{version}.tar.xz",
            hash="844e6d7db8086f793f57618d3d4b68d29d99b16034e71430df3c21cfd3c3542a",
            dependencies=[
                "ninja",
                "meson",
            ],
        )

    def build(self):
        Meson.build(self, meson_params="-Dbenchmarks=disabled -Dtools=enabled")
        self.install(r"COPYING share\doc\orc")


@project_add
class GstPluginsBase(Tarball, Meson):
    def __init__(self):
        Project.__init__(
            self,
            "gst-plugins-base",
            repository="https://gitlab.freedesktop.org/gstreamer/gstreamer",
            version="1.20.5",
            archive_url="https://gstreamer.freedesktop.org/src/gst-plugins-base/gst-plugins-base-{version}.tar.xz",
            hash="11f911ef65f3095d7cf698a1ad1fc5242ac3ad6c9270465fb5c9e7f4f9c19b35",
            dependencies=["meson", "ninja", "gstreamer", "opus"],
        )
        # Examples depend on GTK3
        self.add_param("-Dexamples=disabled")

        if self.opts.enable_gi:
            self.add_dependency("gobject-introspection")
            enable_gi = "enabled"
        else:
            enable_gi = "disabled"

        self.add_param(f"-Dintrospection={enable_gi}")

    def build(self):
        Meson.build(self)
        self.install(r".\COPYING share\doc\gst-plugins-base")


@project_add
class GstPluginsGood(Tarball, Meson):
    def __init__(self):
        Project.__init__(
            self,
            "gst-plugins-good",
            repository="https://gitlab.freedesktop.org/gstreamer/gstreamer",
            version="1.20.5",
            archive_url="https://gstreamer.freedesktop.org/src/gst-plugins-good/gst-plugins-good-{version}.tar.xz",
            hash="e83ab4d12ca24959489bbb0ec4fac9b90e32f741d49cda357cb554b2cb8b97f9",
            dependencies=[
                "meson",
                "ninja",
                "glib",
                "gstreamer",
                "gst-plugins-base",
                "libvpx",
            ],
        )

    def build(self):
        Meson.build(self)
        self.install(r".\COPYING share\doc\gst-plugins-good")


@project_add
class GstPluginsBad(Tarball, Meson):
    def __init__(self):
        Project.__init__(
            self,
            "gst-plugins-bad",
            repository="https://gitlab.freedesktop.org/gstreamer/gstreamer",
            version="1.20.5",
            archive_url="https://gstreamer.freedesktop.org/src/gst-plugins-bad/gst-plugins-bad-{version}.tar.xz",
            hash="f431214b0754d7037adcde93c3195106196588973e5b32dcb24938805f866363",
            dependencies=["meson", "ninja", "glib", "gstreamer", "gst-plugins-base"],
            patches=[
                "wasapisink-reduce-buffer-latency.patch",
            ],
        )
        self.add_param("-Dcurl=disabled")
        self.add_param("-Dcurl-ssh2=disabled")

    def build(self):
        Meson.build(self)
        self.install(r".\COPYING share\doc\gst-plugins-bad")


@project_add
class GstPython(Tarball, Meson):
    def __init__(self):
        Project.__init__(
            self,
            "gst-python",
            repository="https://gitlab.freedesktop.org/gstreamer/gstreamer",
            version="1.20.5",
            archive_url="https://gstreamer.freedesktop.org/src/gst-python/gst-python-{version}.tar.xz",
            hash="27487652318659cfd7dc42784b713c78d29cc7a7df4fb397134c8c125f65e3b2",
            dependencies=["meson", "ninja", "glib", "gstreamer", "pygobject"],
        )

    def build(self):
        Meson.build(self)
        self.install(r".\COPYING share\doc\gst-python")
