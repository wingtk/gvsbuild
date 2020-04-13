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
from .simple_ui import log
from .base_expanders import Tarball, MercurialRepo
from .base_project import Project

class Meson(Project):
    def __init__(self, name, **kwargs):
        Project.__init__(self, name, **kwargs)
        self._ensure_params()

    def _ensure_params(self):
        if not hasattr(self, 'params'):
            self.params = []
                    
    def add_param(self, par):
        self._ensure_params()
        self.params.append(par)

    def build(self, meson_params=None, make_tests=False, add_path=None):
        # where we build, with ninja, the library
        ninja_build = os.path.join(self.build_dir, '_gvsbuild-meson')

        # First we check if we need to generate the meson build files
        if not os.path.isfile(os.path.join(ninja_build, 'build.ninja')):
            log.start_verbose('Generating meson directory')
            self.builder.make_dir(ninja_build)
            # base params 
            self._ensure_params()
            if self.params:
                add_opts = ' '.join(self.params) + ' '
            else:
                add_opts = ''
            # debug info
            add_opts += '--buildtype ' + ('debug' if self.builder.opts.configuration == 'debug' else 'debugoptimized')
            if meson_params:
                add_opts += ' ' + meson_params
            # pyhon meson.py src_dir ninja_build_dir --prefix gtk_bin options
            meson = Project.get_tool_executable('meson')
            python = Project.get_tool_executable('python')
            cmd = '%s %s %s %s --prefix %s %s' % (python, meson, self._get_working_dir(), ninja_build, self.builder.gtk_dir, add_opts, )
            # build the ninja file to do everything (build the library, create the .pc file, install it, ...)
            self.exec_vs(cmd, add_path=add_path)
            log.end()
            
        if make_tests:
            # Run ninja to build all (library, ....
            self.builder.exec_ninja(working_dir=ninja_build)
            # .. run the tests ...
            self.builder.exec_ninja(params='test', working_dir=ninja_build)
            # .. and finally install everything
        # if we don't make the tests we simply run 'ninja install' that takes care of everything, running explicity from the build dir
        self.builder.exec_ninja(params='install', working_dir=ninja_build)

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
            cmake_dir = os.path.join(self.build_dir, '_gvsbuild-cmake')

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
        log.start_verbose('Generating/updating cmake files')
        self.builder.exec_vs(cmd, working_dir=work_dir)
        log.end()
        # Build
        if use_ninja:
            if make_tests:
                self.builder.exec_ninja(working_dir=work_dir)
                self.builder.exec_ninja(params='test', working_dir=work_dir)
                if do_install:
                    self.builder.exec_ninja(params='install', working_dir=work_dir)
            else:
                if do_install:
                    self.builder.exec_ninja(params='install', working_dir=work_dir)
                else:
                    self.builder.exec_ninja(working_dir=work_dir)
        else:
            self.builder.exec_vs('nmake /nologo', working_dir=work_dir)
            if do_install:
                self.builder.exec_vs('nmake /nologo install', working_dir=work_dir)

class MercurialCmakeProject(MercurialRepo, CmakeProject):
    def __init__(self, name, **kwargs):
        CmakeProject.__init__(self, name, **kwargs)

class Rust(Project):
    def __init__(self, name, **kwargs):
        Project.__init__(self, name, **kwargs)
        self._ensure_params()

    def _ensure_params(self):
        if not hasattr(self, 'params'):
            self.params = []

    def add_param(self, par):
        self._ensure_params()
        self.params.append(par)

    def build(self, cargo_params=None, make_tests=False):
        rustc_opts = {}

        if cargo_params:
            params = cargo_params[:]
        else:
            params = []

        if self.builder.opts.configuration == 'release':
            # add debug symbols anyway
            rustc_opts['RUSTFLAGS'] = '-g'
            params.append('--release')
            folder = 'release'
        else:
            folder = 'debug'

        cargo_build = os.path.join(self.build_dir, 'cargo-build')

        params.append('--target-dir=%s' % cargo_build)

        if self.clean and os.path.exists(cargo_build):
            log.debug("Removing cargo build dir '%s'" % cargo_build)
            shutil.rmtree(cargo_build, onerror=_rmtree_error_handler)

        # build
        self.builder.exec_cargo(params=' '.join(['build'] + params), working_dir=self.build_dir, rustc_opts=rustc_opts)

        # test
        if make_tests:
            self.builder.exec_cargo(params=' '.join(['test'] + params), working_dir=self.build_dir, rustc_opts=rustc_opts)

        shutil.copytree(os.path.join(cargo_build, folder),
                        os.path.join(cargo_build, 'lib'))
