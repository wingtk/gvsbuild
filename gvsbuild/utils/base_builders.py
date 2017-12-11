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

"""
Various builders (meson, CMake, ...) class
"""

import os
import shutil

from .utils import _rmtree_error_handler
from .simple_ui import print_debug
from .base_expanders import Tarball, MercurialRepo
from .base_project import Project

class Meson(Project):
    def __init__(self, name, **kwargs):
        Project.__init__(self, name, **kwargs)

    def build(self, meson_params=None, make_tests=False):
        # where we build, with ninja, the library
        ninja_build = self.build_dir + '-meson'
        # clean up and regenerate all
        if self.builder.opts.clean and os.path.exists(ninja_build):
            print_debug("Removing meson build dir '%s'" % (ninja_build, ))
            shutil.rmtree(ninja_build, onerror=_rmtree_error_handler)

        # First we check if we need to generate the meson build files
        if not os.path.isfile(os.path.join(ninja_build, 'build.ninja')):
            self.builder.make_dir(ninja_build)
            # debug info
            add_opts = '--buildtype ' + self.builder.opts.configuration
            if meson_params:
                add_opts += ' ' + meson_params
            # pyhon meson.py src_dir ninja_build_dir --prefix gtk_bin options
            cmd = '%s\\python.exe %s %s %s --prefix %s %s' % (self.builder.opts.python_dir, self.builder.meson, self.build_dir, ninja_build, self.builder.gtk_dir, add_opts, )
            # build the ninja file to do everything (build the library, create the .pc file, install it, ...)
            self.exec_vs(cmd)

        if make_tests:
            # Run ninja to build all (library, ....
            self.builder.exec_vs('ninja', working_dir=ninja_build)
            # .. run the tests ...
            self.builder.exec_vs('ninja test', working_dir=ninja_build)
            # .. and finally install everything
        # if we don't make the tests we simply run 'ninja install' that takes care of everything, running explicity from the build dir
        self.builder.exec_vs('ninja install', working_dir=ninja_build)

class CmakeProject(Project):
    def __init__(self, name, **kwargs):
        Project.__init__(self, name, **kwargs)

    def build(self, cmake_params=None, use_ninja=False, make_tests=False, do_install=True, out_of_source=None, source_part=None):
        cmake_config = 'Debug' if self.builder.opts.configuration == 'debug' else 'RelWithDebInfo'
        cmake_gen = 'Ninja' if use_ninja else 'NMake Makefiles'

        # Create the command for cmake
        cmd = 'cmake -G "' + cmake_gen + '" -DCMAKE_INSTALL_PREFIX="%(pkg_dir)s" -DGTK_DIR="%(gtk_dir)s" -DCMAKE_BUILD_TYPE=' + cmake_config
        if cmake_params:
            cmd += ' ' + cmake_params
        if use_ninja and out_of_source is None:
            # For ninja the default is build out of source
            out_of_source = True

        if out_of_source:
            cmake_dir = self.build_dir + '-cmake'

            # clean up and regenerate all
            if self.builder.opts.clean and os.path.exists(cmake_dir):
                print_debug("Removing cmake build dir '%s'" % (cmake_dir, ))
                shutil.rmtree(cmake_dir, onerror=_rmtree_error_handler)

            self.builder.make_dir(cmake_dir)
            if source_part:
                src_full = os.path.join(self.build_dir, source_part)
            else:
                src_full = self.build_dir
            cmd += ' -B%s -H%s' % (cmake_dir, src_full, )
            work_dir = cmake_dir
        else:
            work_dir = self._get_working_dir()

        # Generate the files used to build
        self.builder.exec_vs(cmd, working_dir=work_dir)
        # Build
        if use_ninja:
            if make_tests:
                self.builder.exec_vs('ninja', working_dir=work_dir)
                self.builder.exec_vs('ninja test', working_dir=work_dir)
                if do_install:
                    self.builder.exec_vs('ninja install', working_dir=work_dir)
            else:
                if do_install:
                    self.builder.exec_vs('ninja install', working_dir=work_dir)
                else:
                    self.builder.exec_vs('ninja', working_dir=work_dir)
        else:
            self.builder.exec_vs('nmake /nologo', working_dir=work_dir)
            if do_install:
                self.builder.exec_vs('nmake /nologo install', working_dir=work_dir)

class MercurialCmakeProject(MercurialRepo, CmakeProject):
    def __init__(self, name, **kwargs):
        CmakeProject.__init__(self, name, **kwargs)
