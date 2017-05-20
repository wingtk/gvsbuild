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

from .utils.base_tool import Tool
from .utils.base_expanders import extract_exec

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
        destfile = os.path.join(self.cmake_path, 'bin', 'cmake.exe')
        extract_exec(self.archive_file, self.builder.opts.tools_root_dir, dir_part = self.dir_part, check_file = destfile, check_mark=True)

    def get_path(self):
        return os.path.join(self.cmake_path, 'bin')

Tool.add(Tool_cmake())

class Tool_meson(Tool):
    def __init__(self):
        Tool.__init__(self,
            'meson',
            archive_url = 'https://github.com/mesonbuild/meson/archive/0.40.1.zip',
            hash = '27c977e79b212f174b70f15b61a3407f283fe4dd3a5d41b6715ff522835fd3d0',
            dir_part = 'meson-0.40.1')

    def load_defaults(self, builder):
        Tool.load_defaults(self, builder)
        # Set the builder object to point to the file to use
        builder.meson = os.path.join(self.build_dir, 'meson.py')

    def unpack(self):
        extract_exec(self.archive_file, self.builder.opts.tools_root_dir, dir_part = self.dir_part, check_file = self.builder.meson, check_mark=True)

    def get_path(self):
        pass

Tool.add(Tool_meson())

class Tool_nasm(Tool):
    def __init__(self):
        Tool.__init__(self,
            'nasm',
            archive_url = 'http://www.nasm.us/pub/nasm/releasebuilds/2.13.01/win64/nasm-2.13.01-win64.zip',
            hash = '8b368c5ed7f9deb33be90918e8c19b2fbf004fbe74b743e515674c75943d3362',
            dir_part = 'nasm-2.13.01')

    def load_defaults(self, builder):
        Tool.load_defaults(self, builder)
        self.nasm_path = self.build_dir

    def unpack(self):
        # We download directly the exe file so we copy it on the tool directory ...
        destfile = os.path.join(self.build_dir, 'nasm.exe')
        extract_exec(self.archive_file, self.builder.opts.tools_root_dir, dir_part = self.dir_part, check_file = destfile, force_dest = destfile)

    def get_path(self):
        return self.nasm_path

Tool.add(Tool_nasm())

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
        destfile = os.path.join(self.ninja_path, 'ninja.exe')
        extract_exec(self.archive_file, self.ninja_path, check_file = destfile, check_mark=True)

    def get_path(self):
        return self.ninja_path

Tool.add(Tool_ninja())

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
        extract_exec(self.archive_file, self.build_dir, check_file = self.builder.nuget, check_mark=True)

    def get_path(self):
        # No need to add the path, we use the full file name
        pass

Tool.add(Tool_nuget())

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
        destfile = os.path.join(self.perl_path, 'perl.exe')
        extract_exec(self.archive_file, self.build_dir, check_file = destfile, check_mark=True)

    def get_path(self):
        return self.perl_path

Tool.add(Tool_perl())

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

Tool.add(Tool_python())

class Tool_yasm(Tool):
    def __init__(self):
        Tool.__init__(self,
            'yasm',
            archive_url = 'http://www.tortall.net/projects/yasm/releases/yasm-1.3.0-win64.exe',
            hash = 'd160b1d97266f3f28a71b4420a0ad2cd088a7977c2dd3b25af155652d8d8d91f')

    def load_defaults(self, builder):
        Tool.load_defaults(self, builder)
        self.yasm_path = self.build_dir

    def unpack(self):
        # We download directly the exe file so we copy it on the tool directory ...
        destfile = os.path.join(self.build_dir, 'yasm.exe')
        extract_exec(self.archive_file, self.build_dir, check_file = destfile, force_dest = destfile, check_mark=True)

    def get_path(self):
        return self.yasm_path

Tool.add(Tool_yasm())
