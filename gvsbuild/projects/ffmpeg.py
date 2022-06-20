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
            archive_url="https://ffmpeg.org/releases/ffmpeg-5.0.1.tar.xz",
            hash="ef2efae259ce80a240de48ec85ecb062cecca26e4352ffb3fda562c21a93007b",
            dependencies=["nasm", "msys2", "pkg-config", "nv-codec-headers"],
            patches=["0001-Added-support-for-MB_INFO.patch"],
        )
        if self.opts.ffmpeg_enable_gpl:
            self.add_dependency("x264")

    def build(self):
        msys_path = Project.get_tool_path("msys2")
        self.exec_vs(
            r"%s\bash build\build.sh %s %s %s %s"
            % (
                msys_path,
                convert_to_msys(self.pkg_dir),
                convert_to_msys(self.builder.gtk_dir),
                self.builder.opts.configuration,
                "enable_gpl" if self.opts.ffmpeg_enable_gpl else "disable_gpl",
            ),
            add_path=msys_path,
        )

        self.install(r".\COPYING.LGPLv2.1 " r".\COPYING.LGPLv3 " r"share\doc\ffmpeg")
        if self.opts.ffmpeg_enable_gpl:
            self.install(r".\COPYING.GPLv2 " r"share\doc\ffmpeg")

    def post_install(self):
        self.builder.exec_msys(
            ["mv", "avcodec.lib", "../lib/"],
            working_dir=os.path.join(self.builder.gtk_dir, "bin"),
        )
        self.builder.exec_msys(
            ["mv", "avutil.lib", "../lib/"],
            working_dir=os.path.join(self.builder.gtk_dir, "bin"),
        )
        if self.opts.ffmpeg_enable_gpl:
            self.builder.exec_msys(
                ["mv", "postproc.lib", "../lib/"],
                working_dir=os.path.join(self.builder.gtk_dir, "bin"),
            )
        self.builder.exec_msys(
            ["mv", "swscale.lib", "../lib/"],
            working_dir=os.path.join(self.builder.gtk_dir, "bin"),
        )


@project_add
class Project_nv_codec_headers(Tarball, Project):
    def __init__(self):
        Project.__init__(
            self,
            "nv-codec-headers",
            archive_url="https://github.com/FFmpeg/nv-codec-headers/releases/download/n11.1.5.1/nv-codec-headers-11.1.5.1.tar.gz",
            hash="a28cdde3ac0e9e02c2dde7a1b4de5333b4ac6148a8332ca712da243a3361a0d9",
            version="11.1.5.1",
        )

    def build(self):
        add_path = os.path.join(self.builder.opts.msys_dir, "usr", "bin")

        self.exec_vs(r'make install PREFIX="%(gtk_dir)s"', add_path=add_path)
