#  Copyright (C) 2016 - Yevgen Muntyan
#  Copyright (C) 2016 - Ignacio Casal Quinteiro
#  Copyright (C) 2016 - Arnavion
#  Copyright (C) 2022 - Alexandros Theodotou
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

@project_add
class Fftw3(Tarball, CmakeProject):
    def __init__(self):
        Project.__init__(
            self,
            "fftw3",
            archive_url="http://www.fftw.org/fftw-3.3.10.tar.gz",
            hash="56c932549852cddcfafdab3820b0200c7742675be92179e59e6215b340e26467",
            dependencies=["cmake", "ninja"],
        )

    def build(self):
        CmakeProject.build(self, use_ninja=True, cmake_params="-DENABLE_THREADS=ON -DENABLE_SSE=ON -DENABLE_SSE2=ON -DENABLE_AVX=ON -DENABLE_AVX2=ON -DWITH_COMBINED_THREADS=ON -DENABLE_FLOAT=OFF")

@project_add
class Fftw3f(Tarball, CmakeProject):
    def __init__(self):
        Project.__init__(
            self,
            "fftw3f",
            archive_url="http://www.fftw.org/fftw-3.3.10.tar.gz",
            hash="56c932549852cddcfafdab3820b0200c7742675be92179e59e6215b340e26467",
            dependencies=["cmake", "ninja"],
        )

    def build(self):
        CmakeProject.build(self, use_ninja=True, cmake_params="-DENABLE_THREADS=ON -DENABLE_SSE=ON -DENABLE_SSE2=ON -DENABLE_AVX=ON -DENABLE_AVX2=ON -DWITH_COMBINED_THREADS=ON -DENABLE_FLOAT=ON")
