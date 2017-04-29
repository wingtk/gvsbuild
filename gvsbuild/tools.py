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
Default tools used to build the various projects
"""

import os
import sys
import shutil
import zipfile

from .utils.utils import convert_to_msys
from .utils.simple_ui import print_log
from .utils.base_tool import Tool
from .utils.base_project import Project

class Tool_cmake(Tool):
    def __init__(self):
        Tool.__init__(self,
            'cmake',
            archive_url = 'https://cmake.org/files/v3.7/cmake-3.7.2-win64-x64.zip',
            hash = 'def3bb81dfd922ce1ea2a0647645eefb60e128d520c8ca707c5996c331bc8b48',
            dir_part = 'cmake-3.7.2-win64-x64')

    def load_defaults(self, builder):
        Tool.load_defaults(self, builder)
        # Set the builder object to point to the file to use
        self.cmake_path = self.build_dir

    def unpack(self):
        # We download a .zip file so we estract it in the tool directory, with the version ...
        destfile = os.path.join(self.cmake_path, 'bin', 'cmake.exe')
        if not os.path.isfile(destfile):
            print_log("Unpacking cmake to tools directory (%s)" % (self.build_dir, ))
            with zipfile.ZipFile(self.archive_file) as zf:
                # In the zip file the dir part (cmake-...) is already present
                zf.extractall(path=self.builder.opts.tools_root_dir)

    def get_path(self):
        return os.path.join(self.cmake_path, 'bin')

Project.add(Tool_cmake())

class Tool_meson(Tool):
    def __init__(self):
        Tool.__init__(self,
            'meson',
            archive_url = 'https://github.com/mesonbuild/meson/archive/0.39.1.zip',
            hash = '4b9653c1cfa3bd5d207ddecbc9d97a2eab2a5321884a9a4d3abc2620a7cce2e6',
            dir_part = 'meson-0.39.1')

    def load_defaults(self, builder):
        Tool.load_defaults(self, builder)
        # Set the builder object to point to the file to use
        builder.meson = os.path.join(self.build_dir, 'meson.py')

    def unpack(self):
        # We download a .zip file so we estract it in the tool directory, with the version ...
        if not os.path.isfile(self.builder.meson):
            destdir = os.path.join(self.builder.opts.tools_root_dir, self.dir_part)
            print_log("Unpacking meson to tools directory (%s)" % (self.build_dir, ))
            self.builder.make_dir(destdir)
            with zipfile.ZipFile(self.archive_file) as zf:
                # In the zip file the dir part (meson-0.xx...) is already present
                zf.extractall(path=self.builder.opts.tools_root_dir)

    def get_path(self):
        pass

Project.add(Tool_meson())

class Tool_ninja(Tool):
    def __init__(self):
        Tool.__init__(self,
            'ninja',
            archive_url = 'https://github.com/ninja-build/ninja/releases/download/v1.7.2/ninja-win.zip',
            hash = '95b36a597d33c1fe672829cfe47b5ab34b3a1a4c6bf628e5d150b6075df4ef50')

    def load_defaults(self, builder):
        Tool.load_defaults(self, builder)
        # Set the builder object to point to the path to use
        self.ninja_path = self.build_dir

    def unpack(self):
        # We download a .zip file so we estract it in the tool directory ...
        destfile = os.path.join(self.ninja_path, 'ninja.exe')
        if not os.path.isfile(destfile):
            print_log("Unpacking ninja to tools directory (%s)" % (self.build_dir, ))
            self.builder.make_dir(self.ninja_path)
            with zipfile.ZipFile(self.archive_file) as zf:
                zf.extractall(path=self.ninja_path)

    def get_path(self):
        return self.ninja_path

Project.add(Tool_ninja())

class Tool_nuget(Tool):
    def __init__(self):
        Tool.__init__(self,
            'nuget',
            archive_url = 'https://dist.nuget.org/win-x86-commandline/latest/nuget.exe',
            hash = '399ec24c26ed54d6887cde61994bb3d1cada7956c1b19ff880f06f060c039918')

    def load_defaults(self, builder):
        Tool.load_defaults(self, builder)
        # Set the builder object to point to the .exe file to use
        builder.nuget = os.path.join(self.build_dir, 'nuget.exe')

    def unpack(self):
        # We download directly the exe file so we copy it on the tool directory ...
        if not os.path.isfile(self.builder.nuget):
            print_log("Copying file to tools directory (%s)" % (self.build_dir, ))
            self.builder.make_dir(self.build_dir)
            shutil.copy2(self.archive_file, self.build_dir)

    def get_path(self):
        # No need to add the path, we use the full file name
        pass

Project.add(Tool_nuget())

class Tool_perl(Tool):
    def __init__(self):
        Tool.__init__(self,
            'perl',
            archive_url = 'https://github.com/wingtk/gtk-win32/releases/download/Perl-5.20/perl-5.20.0-x64.tar.xz',
            hash = '05e01cf30bb47d3938db6169299ed49271f91c1615aeee5649174f48ff418c55')

    def load_defaults(self, builder):
        Tool.load_defaults(self, builder)
        # Set the builder object to point to the path to use, when we need to pass directly
        # the executable to *make
        builder.perl_dir = os.path.join(self.build_dir, 'x64')
        # full path, added to the environment when needed
        self.perl_path = os.path.join(builder.perl_dir, 'bin')

    def unpack(self):
        # We download a tar.xz file so we estract it in the tool directory ...
        destfile = os.path.join(self.perl_path, 'perl.exe')
        if not os.path.isfile(destfile):
            print_log("Unpacking perl to tools directory (%s)" % (self.build_dir, ))
            self.builder.make_dir(self.build_dir)
            self.builder.exec_msys([self.builder.tar, 'xf', convert_to_msys(self.archive_file), '-C', convert_to_msys(self.build_dir)])

    def get_path(self):
        return self.perl_path

Project.add(Tool_perl())

class Tool_python(Tool):
    def __init__(self):
        Tool.__init__(self,
            'python')

    def load_defaults(self, builder):
        Tool.load_defaults(self, builder)
        if builder.opts.python_dir:
            # From the command line, hope is at least 3.4 ...
            self.python_path = builder.opts.python_dir
        else:
            # We use the one that call the script
            self.python_path = os.path.dirname(sys.executable)

    def unpack(self):
        pass

    def get_path(self):
        return self.python_path

Project.add(Tool_python())
