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
            version="1.28.4",
            lastversion_even=True,
            archive_url="https://gstreamer.freedesktop.org/src/gstreamer/gstreamer-{version}.tar.xz",
            hash="f5adc7e8f448c10260b3b25aa101c9d540674c8d9a54c2b77a86d04f2b3b50dd",
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
            self,
            add_path=add_path,
            meson_params=["-Dtests=disabled", "-Dexamples=disabled"],
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
        Meson.build(self, meson_params=["-Dbenchmarks=disabled", "-Dtools=enabled"])
        self.install(r"COPYING share\doc\orc")


@project_add
class GstPluginsBase(Tarball, Meson):
    def __init__(self):
        Project.__init__(
            self,
            "gst-plugins-base",
            repository="https://gitlab.freedesktop.org/gstreamer/gstreamer",
            version="1.28.4",
            lastversion_even=True,
            archive_url="https://gstreamer.freedesktop.org/src/gst-plugins-base/gst-plugins-base-{version}.tar.xz",
            hash="a898afd5766172b0049e6781558e0689098bf87b9d82b846c652e571c01d60d8",
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
            self, meson_params=[f"-Dc_link_args={self.builder.gtk_dir}\\lib\\ogg.lib"]
        )
        self.install(r".\COPYING share\doc\gst-plugins-base")


@project_add
class GstPluginsGood(Tarball, Meson):
    def __init__(self):
        Project.__init__(
            self,
            "gst-plugins-good",
            repository="https://gitlab.freedesktop.org/gstreamer/gstreamer",
            version="1.28.4",
            lastversion_even=True,
            archive_url="https://gstreamer.freedesktop.org/src/gst-plugins-good/gst-plugins-good-{version}.tar.xz",
            hash="c825ea737c59cea0e4a0c41da2388045ff5dd32d162220ac93a7a82ee4a04e61",
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
            version="1.28.4",
            lastversion_even=True,
            archive_url="https://gstreamer.freedesktop.org/src/gst-plugins-bad/gst-plugins-bad-{version}.tar.xz",
            hash="332b7320f30c60f2d5941446d03b9d05e3781f2c2561befbe88718bd777f0e47",
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
            version="1.28.4",
            lastversion_even=True,
            archive_url="https://gstreamer.freedesktop.org/src/gst-plugins-ugly/gst-plugins-ugly-{version}.tar.xz",
            hash="5486cd145c5af43259fd37caca59d048e2a67ddb07082ea8f50ef0f02a85f8a5",
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
            version="1.28.4",
            lastversion_even=True,
            archive_url="https://gstreamer.freedesktop.org/src/gst-devtools/gst-devtools-{version}.tar.xz",
            hash="11d4f1188639d3a9762039065bbb7b2c309b7a8ecc6fa4aed12245568bf00db3",
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
            version="1.28.4",
            lastversion_even=True,
            archive_url="https://gstreamer.freedesktop.org/src/gst-python/gst-python-{version}.tar.xz",
            hash="c4eb382720b4443fb801a53418dff0bd4cd7478716d5ced493504a675b4d09fd",
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
            version="1.28.4",
            lastversion_even=True,
            archive_url="https://gstreamer.freedesktop.org/src/gst-libav/gst-libav-{version}.tar.xz",
            hash="bd17a5df2874a7a58bcbaf7b940223379ad9613624db8ead783db03e74bb904b",
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
            version="1.28.4",
            lastversion_even=True,
            archive_url="https://gstreamer.freedesktop.org/src/gst-rtsp-server/gst-rtsp-server-{version}.tar.xz",
            hash="bfb6780542bf0d402736232aeae6c5a1b943c445775bf40305bcb86ca70705a0",
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
            version="0.15.2",
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
        self.builder.exec_cargo(["install", "cargo-c", "--locked"])
        Meson.build(self)
        self.install(r".\LICENSE-MPL-2.0 share\doc\gst-plugin-gtk4")
