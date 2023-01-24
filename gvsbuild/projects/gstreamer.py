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
            version="1.21.90",
            archive_url="https://gstreamer.freedesktop.org/src/gstreamer/gstreamer-{version}.tar.xz",
            hash="03f96fd9e2b9ad12d8ce780db9b31571509b0db3ed2cb3072d25f3f9b6238608",
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
            dependencies=["ninja", "meson"],
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
            version="1.21.90",
            archive_url="https://gstreamer.freedesktop.org/src/gst-plugins-base/gst-plugins-base-{version}.tar.xz",
            hash="5fb7f4f3da47f30cde0ab17d716e2593477133f2bc3a59f822e0d470ec3644fa",
            dependencies=[
                "meson", 
                "ninja", 
                "gstreamer", 
                "opus",
                "ogg"],
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
        Meson.build(self, 
            meson_params=f"-Dc_link_args={self.builder.gtk_dir}\\lib\\ogg.lib"
        )
        self.install(r".\COPYING share\doc\gst-plugins-base")

@project_add
class GstPluginsGood(Tarball, Meson):
    def __init__(self):
        Project.__init__(
            self,
            "gst-plugins-good",
            repository="https://gitlab.freedesktop.org/gstreamer/gstreamer",
            version="1.21.90",
            archive_url="https://gstreamer.freedesktop.org/src/gst-plugins-good/gst-plugins-good-{version}.tar.xz",
            hash="f9b8b772adad6fb0d3a131ba4ee74696a21636582ace642582d24fb545fbdf95",
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
class GstPluginsUgly(Tarball, Meson):
    def __init__(self):
        Project.__init__(
            self,
            "gst-plugins-ugly",
            repository="https://gitlab.freedesktop.org/gstreamer/gstreamer",
            version="1.21.90",
            archive_url="https://gstreamer.freedesktop.org/src/gst-plugins-ugly/gst-plugins-ugly-{version}.tar.xz",
            hash="e548851e10f58c523f151e7074a30ea1e2f3897fb640e9ca130ed898f47a4d8c",
            dependencies=["meson", "ninja", "gst-plugins-base"],
        )

    def build(self):
        Meson.build(self)
        self.install(r".\COPYING share\doc\gst-plugins-ugly")


@project_add
class GstPluginsBad(Tarball, Meson):
    def __init__(self):
        Project.__init__(
            self,
            "gst-plugins-bad",
            repository="https://gitlab.freedesktop.org/gstreamer/gstreamer",
            version="1.21.90",
            archive_url="https://gstreamer.freedesktop.org/src/gst-plugins-bad/gst-plugins-bad-{version}.tar.xz",
            hash="4f234a734e85f3741b480ccdadf497c2de5ee8d6a17aefc34dd2c66d3f88fe40",
            dependencies=["meson", "ninja", "gst-plugins-base"],
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
class GstDevTools(Tarball, Meson):
    def __init__(self):
        Project.__init__(
            self,
            "gst-devtools",
            repository="https://gitlab.freedesktop.org/gstreamer/gstreamer",
            version="1.21.90",
            archive_url="https://gstreamer.freedesktop.org/src/gst-devtools/gst-devtools-{version}.tar.xz",
            hash="a6221431a98b72c70a29e3d6e431c70e023da998d306675866d2901b3a6c688d",
            dependencies=["meson", "ninja", "json-glib"],
        )

    def build(self):
        Meson.build(self)
        self.install(r".\COPYING share\doc\gst-devtools")
  
@project_add
class GstRtspServer(Tarball, Meson):
    def __init__(self):
        Project.__init__(
            self,
            "gst-rtsp-server",
            repository="https://gitlab.freedesktop.org/gstreamer/rtsp-server",
            version="1.21.90",
            archive_url="https://gstreamer.freedesktop.org/src/gst-rtsp-server/gst-rtsp-server-{version}.tar.xz",
            hash="f1519c2cb103464d297591b6c1b53ba83dd59172f70e46bc1539a7874da3d26f",
            dependencies=["meson", "ninja", "gst-plugins-base"],
        )

    def build(self):
        Meson.build(self)
        self.install(r".\COPYING share\doc\gst-rtsp-server")

@project_add
class GstEditingServices(Tarball, Meson):
    def __init__(self):
        Project.__init__(
            self,
            "gst-editing-services",
            repository="https://gitlab.freedesktop.org/gstreamer/gst-editing-services",
            version="1.21.90",
            archive_url="https://gstreamer.freedesktop.org/src/gst-editing-services/gst-editing-services-{version}.tar.xz",
            hash="f3dfa688e385d5bc7e8d666d617098e981492b8d1bee9d88811950039ce91be0",
            dependencies=["meson", "ninja", "gst-plugins-base"],
        )

    def build(self):
        Meson.build(self)
        self.install(r".\COPYING share\doc\gst-editing-services")

@project_add
class GstPython(Tarball, Meson):
    def __init__(self):
        Project.__init__(
            self,
            "gst-python",
            repository="https://gitlab.freedesktop.org/gstreamer/gstreamer",
            version="1.21.90",
            archive_url="https://gstreamer.freedesktop.org/src/gst-python/gst-python-{version}.tar.xz",
            hash="5927e96a773325ada7c16e6e2649e8a8a702d534b7fd7de119fce04f217fb5b2",
            dependencies=["meson", "ninja", "pygobject", "gst-plugins-base"],
        )

    def build(self):
        Meson.build(self)
        self.install(r".\COPYING share\doc\gst-python")
