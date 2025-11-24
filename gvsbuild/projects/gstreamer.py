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
            version="1.26.7",
            lastversion_even=True,
            archive_url="https://gstreamer.freedesktop.org/src/gstreamer/gstreamer-{version}.tar.xz",
            hash="18a5e214114dc501407697dd458514bba62cadd5414c60f793cf70141a4d0bb3",
            dependencies=["meson", "ninja", "glib", "orc"],
            patches=[],
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
            version="0.4.41",
            lastversion_even=True,
            repository="https://gitlab.freedesktop.org/gstreamer/orc",
            archive_url="https://gstreamer.freedesktop.org/src/orc/orc-{version}.tar.xz",
            hash="cb1bfd4f655289cd39bc04642d597be9de5427623f0861c1fc19c08d98467fa2",
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
            version="1.26.7",
            lastversion_even=True,
            archive_url="https://gstreamer.freedesktop.org/src/gst-plugins-base/gst-plugins-base-{version}.tar.xz",
            hash="969e3cbf05dfab92cf37e94840fbe398517d7ba3275331d1c216a2e30a7208d0",
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
            enable_gi = "enabled"
        else:
            enable_gi = "disabled"

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
            version="1.26.7",
            lastversion_even=True,
            archive_url="https://gstreamer.freedesktop.org/src/gst-plugins-good/gst-plugins-good-{version}.tar.xz",
            hash="82af18a1f3e4a060db61d2630fbb975269b80b55bb2fdcfddfab5c6440d30781",
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
            version="1.26.7",
            lastversion_even=True,
            archive_url="https://gstreamer.freedesktop.org/src/gst-plugins-bad/gst-plugins-bad-{version}.tar.xz",
            hash="a0ab17dddd4c029ecd7a423c30badd5a3c7599ea42707016d1d57545f5723ccf",
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
            enable_gi = "enabled"
        else:
            enable_gi = "disabled"

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
            version="1.26.7",
            lastversion_even=True,
            archive_url="https://gstreamer.freedesktop.org/src/gst-plugins-ugly/gst-plugins-ugly-{version}.tar.xz",
            hash="11f2e4f34bb2e841dc60edc95581572bc47be0c11e577d12bed98bb1f80a661b",
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
            version="1.26.7",
            lastversion_even=True,
            archive_url="https://gstreamer.freedesktop.org/src/gst-devtools/gst-devtools-{version}.tar.xz",
            hash="6912330ecfaf4f4f1329defbe97b9daf92e9aeaf8375e327a0dd30524d79f0a0",
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
            enable_gi = "enabled"
        else:
            enable_gi = "disabled"

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
            version="1.26.7",
            lastversion_even=True,
            archive_url="https://gstreamer.freedesktop.org/src/gst-python/gst-python-{version}.tar.xz",
            hash="7a544b7968b181c2965e979f2ce889db36397790de9a7c312cf468b51d26428c",
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
            version="1.26.7",
            lastversion_even=True,
            archive_url="https://gstreamer.freedesktop.org/src/gst-libav/gst-libav-{version}.tar.xz",
            hash="91d4a7a14527d97fe0ce7ccedb3554e8f692b216429ef2b1850944bbf5435c09",
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
            version="1.26.7",
            lastversion_even=True,
            archive_url="https://gstreamer.freedesktop.org/src/gst-rtsp-server/gst-rtsp-server-{version}.tar.xz",
            hash="4f234594aea692e3c1bfaa969965039aaf7483bdfc5862b31d614a59e6718abf",
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
