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

from gvsbuild.utils.base_builders import CmakeProject
from gvsbuild.utils.base_expanders import Tarball
from gvsbuild.utils.base_project import Project, project_add
from gvsbuild.utils.simple_ui import log
import os
import sys
from pathlib import Path
from shutil import copyfile

@project_add
class Libpng(Tarball, CmakeProject):
    def __init__(self):
        name = "libpng"
        Project.__init__(
            self,
            name,
            version="1.6.39",
            archive_url="http://prdownloads.sourceforge.net/libpng/libpng-{version}.tar.xz",
            hash="1f4696ce70b4ee5f85f1e1623dc1229b210029fa4b7aee573df3e2ba7b036937",
            dependencies=["cmake", "ninja", "zlib"],
        )
        log.message(f"Init() Building LIBPNG {os.path.dirname(os.path.realpath(__file__))}")

    def build(self):
        #
        print(f"{self.name} {self.prj_dir} {self.patch_dir}")
        # root folder
        patch_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
        # the folder containing this file
        patch_dir = os.path.dirname(os.path.realpath(__file__))
        patch_dir += "/../patches/libpng"
        log.message(f"Patches: {patch_dir} {os.path.isdir(patch_dir)}")
        work_dir = self._get_working_dir()
        log.message(f"work_dir: {work_dir}")
        log.message(f"self.build_dir: {self.build_dir}")
        cmake_dir = os.path.join(self.build_dir, "_gvsbuild-cmake")
        log.message(f"cmake_dir: {cmake_dir}")


        src=patch_dir+"/checksym.awk"
        pdst=f"{cmake_dir}/scripts"
        dst=pdst + "/checksym.awk"
        log.message(f"*** Building LIBPNG {os.path.dirname(os.path.realpath(__file__))}")

        if not os.path.isdir(pdst):
            os.makedirs(pdst)
            log.message(f"Created: {pdst}  {os.path.isdir(pdst)}")
            if not Path(dst).is_file():
                copyfile(src, dst)
                log.message(f"Copied: {src} {dst} => {Path(dst).is_file()}")

        CmakeProject.build(self, use_ninja=True)

        self.install_pc_files()
        self.install(r"LICENSE share\doc\libpng")
