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
            archive_url="https://gstreamer.freedesktop.org/src/gstreamer/gstreamer-1.20.2.tar.xz",
            hash="df24e8792691a02dfe003b3833a51f1dbc6c3331ae625d143b17da939ceb5e0a",
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
            archive_url="https://gstreamer.freedesktop.org/src/orc/orc-0.4.32.tar.xz",
            hash="a66e3d8f2b7e65178d786a01ef61f2a0a0b4d0b8370de7ce134ba73da4af18f0",
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
            archive_url="https://gstreamer.freedesktop.org/src/gst-plugins-base/gst-plugins-base-1.20.2.tar.xz",
            hash="ab0656f2ad4d38292a803e0cb4ca090943a9b43c8063f650b4d3e3606c317f17",
            dependencies=["meson", "ninja", "gtk3", "gstreamer", "opus"],
        )

    def build(self):
        Meson.build(self)
        self.install(r".\COPYING share\doc\gst-plugins-base")


@project_add
class GstPluginsGood(Tarball, Meson):
    def __init__(self):
        Project.__init__(
            self,
            "gst-plugins-good",
            archive_url="https://gstreamer.freedesktop.org/src/gst-plugins-good/gst-plugins-good-1.20.2.tar.xz",
            hash="83589007bf002b8f9ef627718f308c16d83351905f0db8e85c3060f304143aae",
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
            archive_url="https://gstreamer.freedesktop.org/src/gst-plugins-bad/gst-plugins-bad-1.20.2.tar.xz",
            hash="4adc4c05f41051f8136b80cda99b0d049a34e777832f9fea7c5a70347658745b",
            dependencies=["meson", "ninja", "glib", "gstreamer", "gst-plugins-base"],
            patches=[
                "wasapi-Implement-default-audio-channel-mask.patch",
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
            archive_url="https://gstreamer.freedesktop.org/src/gst-python/gst-python-1.20.2.tar.xz",
            hash="853ea35a1088c762fb703e5aea9c30031a19222b59786b6599956e154620fa2f",
            dependencies=["meson", "ninja", "glib", "gstreamer", "pygobject"],
        )

    def build(self):
        Meson.build(self)
        self.install(r".\COPYING share\doc\gst-python")
