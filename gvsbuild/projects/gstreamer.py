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
            version="1.24.11",
            lastversion_even=True,
            archive_url="https://gstreamer.freedesktop.org/src/gstreamer/gstreamer-{version}.tar.xz",
            hash="093a379602a250d5cd33b88e723757c80198317efde33893edf3c87b6e53b907",
            dependencies=["meson", "ninja", "glib", "orc"],
            patches=[
                "gstpluginloader-win32-fix_use_after_free.patch",
            ],
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
            version="0.4.40",
            lastversion_even=True,
            repository="https://gitlab.freedesktop.org/gstreamer/orc",
            archive_url="https://gstreamer.freedesktop.org/src/orc/orc-{version}.tar.xz",
            hash="3fc2bee78dfb7c41fd9605061fc69138db7df007eae2f669a1f56e8bacef74ab",
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
            version="1.24.11",
            lastversion_even=True,
            archive_url="https://gstreamer.freedesktop.org/src/gst-plugins-base/gst-plugins-base-{version}.tar.xz",
            hash="98572c1f8b710e52673e250cd96e4f2660d79bd66aa172c5dde5f690c1231e1d",
            dependencies=[
                "meson",
                "ninja",
                "gstreamer",
                "opus",
                "ogg",
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
            version="1.24.11",
            lastversion_even=True,
            archive_url="https://gstreamer.freedesktop.org/src/gst-plugins-good/gst-plugins-good-{version}.tar.xz",
            hash="94bf3b5118dd4213af66048faac830569cc9a94a8c8e59e8a6d33b315f518462",
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
            version="1.24.11",
            lastversion_even=True,
            archive_url="https://gstreamer.freedesktop.org/src/gst-plugins-bad/gst-plugins-bad-{version}.tar.xz",
            hash="9126c2b7053a5f059db958f43c6a5230d2e843ff9adff8c8c2477ea2457e3315",
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
            version="1.24.11",
            lastversion_even=True,
            archive_url="https://gstreamer.freedesktop.org/src/gst-plugins-ugly/gst-plugins-ugly-{version}.tar.xz",
            hash="3a1f58a33aee8d13522865bcb564007a6837ef5711d7dfff8ce4260921013f8a",
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
            version="1.24.11",
            lastversion_even=True,
            archive_url="https://gstreamer.freedesktop.org/src/gst-devtools/gst-devtools-{version}.tar.xz",
            hash="73990a939c1ea9d9ca199b8cd135dd3a7120b495004aaa79299257d9cd897834",
            dependencies=["meson", "ninja", "json-glib"],
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
            version="1.24.11",
            lastversion_even=True,
            archive_url="https://gstreamer.freedesktop.org/src/gst-python/gst-python-{version}.tar.xz",
            hash="f4c8761bfee98508f57e2efd738ef36a99e2f7644860877d54d235a7092cf056",
            dependencies=["meson", "ninja", "pygobject", "gst-plugins-base"],
            patches=["0001-fix-python3-not-found.patch"],
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
            version="1.24.11",
            lastversion_even=True,
            archive_url="https://gstreamer.freedesktop.org/src/gst-libav/gst-libav-{version}.tar.xz",
            hash="13776fc16f7ce587d437d56d83e08c9224768dddc897dd3c88208d970a6aa422",
            # TODO try remove gst-plugins-base
            dependencies=["meson", "ninja", "pygobject", "ffmpeg", "gst-plugins-base"],
        )

    def build(self):
        Meson.build(self)
        self.install(r".\COPYING share\doc\gst-libav")
