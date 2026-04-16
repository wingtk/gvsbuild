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
            version="1.28.2",
            lastversion_even=True,
            archive_url="https://gstreamer.freedesktop.org/src/gstreamer/gstreamer-{version}.tar.xz",
            hash="ce5cd44d4ffeafdcc3dddaa072b2179c0b7cb1abf4e6c5d18d4375f8a39fe491",
            dependencies=["meson", "ninja", "glib", "orc"],
            patches=[],
        )

        if self.opts.enable_gi:
            self.add_dependency("gobject-introspection")
        enable_gi = "enabled" if self.opts.enable_gi else "disabled"
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
            version="0.4.42",
            lastversion_even=True,
            repository="https://gitlab.freedesktop.org/gstreamer/orc",
            archive_url="https://gstreamer.freedesktop.org/src/orc/orc-{version}.tar.xz",
            hash="7ec912ab59af3cc97874c456a56a8ae1eec520c385ec447e8a102b2bd122c90c",
            dependencies=["meson", "ninja"],
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
            version="1.28.2",
            lastversion_even=True,
            archive_url="https://gstreamer.freedesktop.org/src/gst-plugins-base/gst-plugins-base-{version}.tar.xz",
            hash="4db76b3619280037a4047de7d9dbb38613a4272dcc40efb333257124635a888d",
            dependencies=[
                "meson",
                "ninja",
                "gstreamer",
                "opus",
                "ogg",
                "graphene",
                "pango",
            ],
        )
        # Examples depend on GTK3
        self.add_param("-Dexamples=disabled")

        if self.opts.enable_gi:
            self.add_dependency("gobject-introspection")
        enable_gi = "enabled" if self.opts.enable_gi else "disabled"
        self.add_param(f"-Dintrospection={enable_gi}")

    def build(self):
        Meson.build(
            self, meson_params=f'-Dc_link_args="{self.builder.gtk_dir}\\lib\\ogg.lib"'
        )
        self.install(r".\COPYING share\doc\gst-plugins-base")


@project_add
class GstPluginsGood(Tarball, Meson):
    def __init__(self):
        Project.__init__(
            self,
            "gst-plugins-good",
            repository="https://gitlab.freedesktop.org/gstreamer/gstreamer",
            version="1.28.2",
            lastversion_even=True,
            archive_url="https://gstreamer.freedesktop.org/src/gst-plugins-good/gst-plugins-good-{version}.tar.xz",
            hash="1ace2d8ec74f632d82eab5006753a27fe0c2402db4ca94d63271e494b62f50bf",
            dependencies=[
                "meson",
                "ninja",
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
            version="1.28.2",
            lastversion_even=True,
            archive_url="https://gstreamer.freedesktop.org/src/gst-plugins-bad/gst-plugins-bad-{version}.tar.xz",
            hash="6467e3964828f4d7d08bfe1fbb4d76287a1c8fa76674e59e101a149c020fefd7",
            dependencies=[
                "meson",
                "ninja",
                "gst-plugins-base",
                "libnice",
                "webrtc-audio-processing",
                "openssl",
                "libsrtp2",
            ],
            patches=[
                "wasapisink-reduce-buffer-latency.patch",
            ],
        )
        self.add_param("-Dcurl=disabled")
        self.add_param("-Dcurl-ssh2=disabled")

        # Adding webrtc-audio-processing adds the isac plugin. It fails to compile.
        self.add_param("-Disac=disabled")

        if self.opts.enable_gi:
            self.add_dependency("gobject-introspection")
        enable_gi = "enabled" if self.opts.enable_gi else "disabled"
        self.add_param(f"-Dintrospection={enable_gi}")

    def build(self):
        Meson.build(self)
        self.install(r".\COPYING share\doc\gst-plugins-bad")


@project_add
class GstPluginsUgly(Tarball, Meson):
    def __init__(self):
        Project.__init__(
            self,
            "gst-plugins-ugly",
            repository="https://gitlab.freedesktop.org/gstreamer/gstreamer",
            version="1.28.2",
            lastversion_even=True,
            archive_url="https://gstreamer.freedesktop.org/src/gst-plugins-ugly/gst-plugins-ugly-{version}.tar.xz",
            hash="fe39a5ee7115e37de9eb65d899ec84c93e6e26ed3ffe25c6d5176cececbab572",
            dependencies=["meson", "ninja", "gst-plugins-base"],
        )

    def build(self):
        Meson.build(self)
        self.install(r".\COPYING share\doc\gst-plugins-ugly")


@project_add
class GstDevTools(Tarball, Meson):
    def __init__(self):
        Project.__init__(
            self,
            "gst-devtools",
            repository="https://gitlab.freedesktop.org/gstreamer/gstreamer",
            version="1.28.2",
            lastversion_even=True,
            archive_url="https://gstreamer.freedesktop.org/src/gst-devtools/gst-devtools-{version}.tar.xz",
            hash="8e012bdcb55503f466d53f1f05e13e8993c69811b9db77cd16a8f6467723bf91",
            dependencies=[
                "meson",
                "ninja",
                "json-glib",
                "gst-plugins-base",
                "gst-plugins-bad",
                "gst-rtsp-server",
            ],
        )

        if self.opts.enable_gi:
            self.add_dependency("gobject-introspection")
        enable_gi = "enabled" if self.opts.enable_gi else "disabled"
        self.add_param(f"-Dintrospection={enable_gi}")

    def build(self):
        Meson.build(self)
        self.install(r".\COPYING share\doc\gst-devtools")


@project_add
class GstPython(Tarball, Meson):
    def __init__(self):
        Project.__init__(
            self,
            "gst-python",
            repository="https://gitlab.freedesktop.org/gstreamer/gstreamer",
            version="1.28.2",
            lastversion_even=True,
            archive_url="https://gstreamer.freedesktop.org/src/gst-python/gst-python-{version}.tar.xz",
            hash="12fdd8e19af97d797a6b2c195228e6c9edc4cddfa68274912b78ef66068ad822",
            dependencies=[
                "meson",
                "ninja",
                "pygobject",
                "gst-plugins-base",
                "gst-plugins-bad",
                "gst-rtsp-server",
            ],
        )

    def build(self):
        Meson.build(self)
        self.install(r".\COPYING share\doc\gst-python")


@project_add
class GstLibav(Tarball, Meson):
    def __init__(self):
        Project.__init__(
            self,
            "gst-libav",
            repository="https://gitlab.freedesktop.org/gstreamer/gstreamer",
            version="1.28.2",
            lastversion_even=True,
            archive_url="https://gstreamer.freedesktop.org/src/gst-libav/gst-libav-{version}.tar.xz",
            hash="45ba65535870aa7c026119d2e90b35dc760e1cf6f50bffbfe8d71223a3043a4e",
            # TODO try remove gst-plugins-base
            dependencies=["meson", "ninja", "pygobject", "ffmpeg", "gst-plugins-base"],
        )

    def build(self):
        Meson.build(self)
        self.install(r".\COPYING share\doc\gst-libav")


@project_add
class GstRtspServer(Tarball, Meson):
    def __init__(self):
        Project.__init__(
            self,
            "gst-rtsp-server",
            repository="https://gitlab.freedesktop.org/gstreamer/gstreamer",
            version="1.28.2",
            lastversion_even=True,
            archive_url="https://gstreamer.freedesktop.org/src/gst-rtsp-server/gst-rtsp-server-{version}.tar.xz",
            hash="917c58b9ff14f91a6b5cd1c3af16c9fcfdf5d8d78d3d167c7e8fa5bdda35f947",
            dependencies=["meson", "ninja", "gstreamer"],
        )

    def build(self):
        Meson.build(self)
        self.install(r".\COPYING share\doc\gst-rtsp-server")


@project_add
class GstPluginGtk4(Tarball, Meson):
    def __init__(self):
        Project.__init__(
            self,
            "gst-plugin-gtk4",
            version="0.14.3",
            repository="https://gitlab.freedesktop.org/gstreamer/gst-plugins-rs",
            archive_url="https://gitlab.freedesktop.org/gstreamer/gst-plugins-rs/-/archive/{version}/gst-plugins-rs-{version}.tar.gz?ref_type=tags",
            archive_filename="gst-plugins-rs-{version}.tar.gz",
            hash="0609b2459ec29f4678edd98e69b6b0a473ef4a303d60645260245dbc23f75167",
            dependencies=[
                "meson",
                "cargo",
                "gst-plugins-base",
                "gst-plugins-bad",
                "gtk4",
            ],
        )
        self.add_param("-Dgtk4=enabled")
        self.add_param("--auto-features=disabled")

    def build(self):
        self.builder.exec_cargo("install cargo-c --locked")
        Meson.build(self)
        self.install(r".\LICENSE-MPL-2.0 share\doc\gst-plugin-gtk4")
