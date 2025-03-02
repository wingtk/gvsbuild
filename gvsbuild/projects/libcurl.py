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

from gvsbuild.utils.base_builders import CmakeProject
from gvsbuild.utils.base_expanders import Tarball
from gvsbuild.utils.base_project import Project, project_add
from gvsbuild.utils.utils import file_replace


@project_add
class Libcurl(Tarball, CmakeProject):
    def __init__(self):
        Project.__init__(
            self,
            "libcurl",
            version="8.12.1",
            repository="https://github.com/curl/curl",
            archive_url="https://github.com/curl/curl/releases/download/curl-{major}_{minor}_{micro}/curl-{version}.tar.xz",
            hash="0341f1ed97a26c811abaebd37d62b833956792b7607ea3f15d001613c76de202",
            dependencies=[
                "perl",
                "cmake",
                "ninja",
                "libpsl",
            ],
        )

    def build(self):
        CmakeProject.build(self, use_ninja=True, cmake_params="-DUSE_WIN32_IDN=ON")
        # Fix the pkg-config .pc file, correcting the library's names
        file_replace(
            os.path.join(self.pkg_dir, "lib", "pkgconfig", "libcurl.pc"),
            [
                (" -lcurl", " -llibcurl_imp"),
            ],
        )

        self.install(r".\COPYING share\doc\libcurl")
