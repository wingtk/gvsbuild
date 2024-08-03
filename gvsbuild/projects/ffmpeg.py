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

import os

from gvsbuild.utils.base_expanders import Tarball
from gvsbuild.utils.base_project import Project, project_add
from gvsbuild.utils.utils import convert_to_msys


@project_add
class Ffmpeg(Tarball, Project):
    def __init__(self):
        Project.__init__(
            self,
            "ffmpeg",
            version="7.0.2",
            archive_url="https://ffmpeg.org/releases/ffmpeg-{version}.tar.xz",
            hash="8646515b638a3ad303e23af6a3587734447cb8fc0a0c064ecdb8e95c4fd8b389",
            dependencies=[
                "dav1d",
                "nasm",
                "msys2",
                "pkgconf",
                "nv-codec-headers",
            ],
            patches=[],
        )
        if self.opts.ffmpeg_enable_gpl:
            self.add_dependency("x264")

    def build(self):
        configuration = (
            "debug-optimized"
            if self.opts.release_configuration_is_actually_debug_optimized
            else self.opts.configuration
        )
        msys_path = Project.get_tool_path("msys2")
        self.exec_vs(
            r"%s\bash build\build.sh %s %s %s %s"
            % (
                msys_path,
                convert_to_msys(self.pkg_dir),
                convert_to_msys(self.builder.gtk_dir),
                configuration,
                "enable_gpl" if self.opts.ffmpeg_enable_gpl else "disable_gpl",
            ),
            add_path=msys_path,
        )

        if configuration in ["debug-optimized", "debug"]:
            self.install(r".\libavcodec\avcodec-60.pdb bin")
            self.install(r".\libavutil\avutil-58.pdb bin")
            self.install(r".\libswscale\libswscale-7.pdb bin")

        self.install(r".\COPYING.LGPLv2.1 " r".\COPYING.LGPLv3 " r"share\doc\ffmpeg")
        if self.opts.ffmpeg_enable_gpl:
            self.install(r".\COPYING.GPLv2 " r"share\doc\ffmpeg")

    def post_install(self):
        for lib in ["avcodec.lib", "avutil.lib", "swscale.lib"]:
            self.builder.exec_msys(
                ["mv", lib, "../lib/"],
                working_dir=os.path.join(self.builder.gtk_dir, "bin"),
            )


@project_add
class NvCodecHeaders(Tarball, Project):
    def __init__(self):
        Project.__init__(
            self,
            "nv-codec-headers",
            version="12.2.72.0",
            archive_url="https://github.com/FFmpeg/nv-codec-headers/releases/download/n{version}/nv-codec-headers-{version}.tar.gz",
            hash="c295a2ba8a06434d4bdc5c2208f8a825285210d71d91d572329b2c51fd0d4d03",
        )

    def build(self):
        add_path = os.path.join(self.builder.opts.msys_dir, "usr", "bin")

        self.exec_vs(r'make install PREFIX="%(gtk_dir)s"', add_path=add_path)
