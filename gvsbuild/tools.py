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
import shutil
import sys
import subprocess

from .utils.base_tool import Tool, tool_add
from .utils.base_expanders import extract_exec
from .utils.base_project import Project
from .utils.simple_ui import log

@tool_add
class Tool_cargo(Tool):
    def __init__(self):
        Tool.__init__(self,
            'cargo',
            archive_url = 'https://win.rustup.rs/x86_64',
            archive_file_name = 'rustup-init.exe',
            exe_name = 'cargo.exe')

    def load_defaults(self):
        Tool.load_defaults(self)
        self.tool_path = os.path.join(self.build_dir, 'bin')
        self.full_exe = os.path.join(self.tool_path, 'cargo.exe')

        self.add_extra_env('RUSTUP_HOME', self.build_dir)
        self.add_extra_env('CARGO_HOME', self.build_dir)

    def unpack(self):
        env = os.environ.copy()
        env['RUSTUP_HOME'] = self.build_dir
        env['CARGO_HOME'] = self.build_dir

        rustup = os.path.join(self.build_dir, 'bin', 'rustup.exe')

        subprocess.check_call('%s --no-modify-path -y' % self.archive_file, shell=True, env=env)

        # add supported targets
        subprocess.check_call('%s target add x86_64-pc-windows-msvc' % rustup, shell=True, env=env)
        subprocess.check_call('%s target add i686-pc-windows-msvc' % rustup, shell=True, env=env)

        # switch to the right target
        subprocess.check_call('%s default stable-%s-pc-windows-msvc' % (rustup, 'i686' if self.opts.x86 else 'x86_64'), env=env)
        
        self.mark_deps = True

@tool_add
class Tool_depot(Tool):
    def __init__(self):
        Tool.__init__(self,
            'depot',
            archive_url = 'https://storage.googleapis.com/chrome-infra/depot_tools.zip',
            skip_hash = True,
            dir_part = 'depot_tools')

    def load_defaults(self):
        Tool.load_defaults(self)
        self.add_extra_env('DEPOT_TOOLS_WIN_TOOLCHAIN', '0')

    def unpack(self):
        self.tool_path = os.path.join(self.opts.tools_root_dir, "depot_tools")
        self.mark_deps = extract_exec(self.archive_file, self.tool_path, dir_part=self.dir_part, check_file = None, check_mark=True)


@tool_add
class Tool_cmake(Tool):
    def __init__(self):
        Tool.__init__(self,
            'cmake',
            archive_url = 'https://cmake.org/files/v3.20/cmake-3.20.0-windows-x86_64.zip',
            hash = '056378cb599353479c3a8aa2654454b8a3eaa3c8c0872928ba7e09c3ec50774c',
            dir_part = 'cmake-3.20.0-windows-x86_64')

    def load_defaults(self):
        Tool.load_defaults(self)
        self.tool_path = os.path.join(self.build_dir, 'bin')
        self.full_exe = os.path.join(self.tool_path, 'cmake.exe')

    def unpack(self):
        self.mark_deps = extract_exec(self.archive_file, self.opts.tools_root_dir, dir_part = self.dir_part, check_file = self.full_exe, check_mark=True)

@tool_add
class Tool_meson(Tool):
    def __init__(self):
        Tool.__init__(self,
            'meson',
            archive_url = 'https://github.com/mesonbuild/meson/archive/refs/tags/0.57.1.tar.gz',
            archive_file_name = 'meson-0.57.1.tar.gz',
            hash = '0c043c9b5350e9087cd4f6becf6c0d10b1d618ca3f919e0dcca2cdf342360d5d',
            dependencies = [ 'python', ],
            dir_part = 'meson-0.57.1',
            exe_name = 'meson.py')

    def unpack(self):
        self.mark_deps = extract_exec(self.archive_file, self.builder.opts.tools_root_dir, dir_part = self.dir_part, check_file = self.full_exe, check_mark=True)

@tool_add
class Tool_msys2(Tool):
    def __init__(self):
        Tool.__init__(self,
            'msys2')

    def load_defaults(self):
        Tool.load_defaults(self)
        self.tool_path = os.path.join(self.opts.msys_dir, 'usr', 'bin')

    def unpack(self):
        self.tool_mark()

    def get_path(self):
        # We always put msys at the end of path
        return None, self.tool_path

@tool_add
class Tool_nasm(Tool):
    def __init__(self):
        Tool.__init__(self,
            'nasm',
            archive_url = 'https://www.nasm.us/pub/nasm/releasebuilds/2.15.05/win64/nasm-2.15.05-win64.zip',
            hash = 'f5c93c146f52b4f1664fa3ce6579f961a910e869ab0dae431bd871bdd2584ef2',
            dir_part = 'nasm-2.15.05',
            exe_name = 'nasm.exe')

    def unpack(self):
        # We download directly the exe file so we copy it on the tool directory ...
        self.mark_deps = extract_exec(self.archive_file, self.builder.opts.tools_root_dir, dir_part = self.dir_part, check_file = self.full_exe, force_dest = self.full_exe, check_mark=True)

@tool_add
class Tool_ninja(Tool):
    def __init__(self):
        Tool.__init__(self,
            'ninja',
            archive_url = 'https://github.com/ninja-build/ninja/releases/download/v1.8.2/ninja-win.zip',
            archive_file_name = 'ninja-win-1.8.2.zip',
            hash = 'c80313e6c26c0b9e0c241504718e2d8bbc2798b73429933adf03fdc6d84f0e70',
            dir_part = 'ninja-1.8.2',
            exe_name = 'ninja.exe')

    def unpack(self):
        self.mark_deps = extract_exec(self.archive_file, self.build_dir, check_file = self.full_exe, check_mark=True)

@tool_add
class Tool_nuget(Tool):
    def __init__(self):
        Tool.__init__(self,
            'nuget',
            archive_url = 'https://dist.nuget.org/win-x86-commandline/v5.4.0/nuget.exe',
            archive_file_name = 'nuget-5.4.0.exe',
            hash = '880f8d306a65932b11f7edd7768b57d20e78fc618b21d785b303da27facc9a70',
            dir_part = 'nuget-5.4.0',
            exe_name = 'nuget.exe')

    def unpack(self):
        # We download directly the exe file so we copy it on the tool directory ...
        self.mark_deps = extract_exec(self.archive_file, self.build_dir, check_file = self.full_exe, force_dest = self.full_exe, check_mark=True)

@tool_add
class Tool_perl(Tool):
    def __init__(self):
        Tool.__init__(self,
            'perl',
            archive_url = 'https://github.com/wingtk/gtk-win32/releases/download/Perl-5.20/perl-5.20.0-x64.tar.xz',
            hash = '05e01cf30bb47d3938db6169299ed49271f91c1615aeee5649174f48ff418c55',
            dir_part = 'perl-5.20.0',
            )

    def load_defaults(self):
        Tool.load_defaults(self)
        # Set the builder object to point to the path to use, when we need to pass directly the executable to *make
        self.base_dir = os.path.join(self.build_dir, 'x64')
        # full path, added to the environment when needed
        self.tool_path = os.path.join(self.base_dir, 'bin')
        self.full_exe = os.path.join(self.tool_path, 'perl.exe')

    def unpack(self):
        self.mark_deps = extract_exec(self.archive_file, self.build_dir, check_file = self.full_exe, check_mark=True)

    def get_base_dir(self):
        return self.base_dir

@tool_add
class Tool_python(Tool):
    def __init__(self):
        Tool.__init__(self,
            'python',
            dependencies = [ 'nuget', ],
            )

    def setup(self, install):
        """
        Using nuget install, locally, the specified version of python
        """
        version = self.opts.python_ver;
        # Get the last version we ask
        if version == '3.5':
            version = '3.5.4'
        elif version == '3.6':
            version = '3.6.8'
        elif version == '3.7':
            version = '3.7.9'
        elif version == '3.8':
            version = '3.8.8'
        elif version == '3.9':
            version = '3.9.2'

        if self.opts.x86:
            name = 'pythonx86'
        else:
            name = 'python'
        t_id = name + '.' + version
        dest_dir = os.path.join(self.opts.tools_root_dir, t_id)
        # directory to use for the .exe
        self.tool_path = os.path.join(dest_dir, 'tools')
        self.full_exe = os.path.join(self.tool_path, 'python.exe')

        if install:
            # see if it's already ok
            rd_file = ''
            try:
                with open(os.path.join(dest_dir, '.wingtk-extracted-file'), 'rt') as fi:
                    rd_file = fi.readline().strip()
            except IOError:
                pass
    
            if rd_file == t_id:
                # Ok, exit
                log.log("Skipping python setup on '%s'" % (dest_dir, ))
                # We don't rebuild the projects that depends on this
                return False
    
            # nuget
            nuget = Project.get_tool_executable('nuget')
            # Install python
            cmd = '%s install %s -Version %s -OutputDirectory %s' % (nuget, name, version, self.opts.tools_root_dir, )
            subprocess.check_call(cmd, shell=True)
            py = os.path.join(self.tool_path, 'python.exe')
    
            # Update pip
            cmd = py + ' -m pip install --upgrade pip'
            if version >= '3.6':
                cmd += ' --no-warn-script-location'
            subprocess.check_call(cmd, shell=True)
    
            # update setuptools (to use vs2017 with python 3.5)
            cmd = py + ' -m pip install --upgrade setuptools --no-warn-script-location'
            subprocess.check_call(cmd, shell=True)
    
            # install/update wheel
            cmd = py + ' -m pip install --upgrade wheel --no-warn-script-location'
            subprocess.check_call(cmd, shell=True)

            python3 = os.path.join(self.tool_path, 'python3.exe')
            if not os.path.exists(python3):
                # We create a python3.exe file so meson find our python and not some other 
                # lying around (e.g. one from the Visual Studio installation ...)
                log.log("Create python3 copy on '%s'" % (dest_dir, ))
                shutil.copy(self.full_exe, python3)

            # Mark that we have done all
            with open(os.path.join(dest_dir, '.wingtk-extracted-file'), 'wt') as fo:
                fo.write('%s\n' % (t_id, ))

        return True

    def load_defaults(self):
        Tool.load_defaults(self)
        self.setup(False)

    def unpack(self):
        if self.opts._load_python:
            # Get python version
            self.mark_deps = self.setup(True)
        else:
            if self.opts.python_dir:
                # From the command line, hope is at least 3.4 ...
                self.tool_path = self.opts.python_dir
            else:
                # We use the one that call the script
                self.tool_path = os.path.dirname(sys.executable)
            self.full_exe = os.path.join(self.tool_path, 'python.exe')
            self.mark_deps = False

@tool_add
class Tool_yasm(Tool):
    def __init__(self):
        Tool.__init__(self,
            'yasm',
            archive_url = 'http://www.tortall.net/projects/yasm/releases/yasm-1.3.0-win64.exe',
            hash = 'd160b1d97266f3f28a71b4420a0ad2cd088a7977c2dd3b25af155652d8d8d91f',
            dir_part = 'yasm-1.3.0',
            exe_name = 'yasm.exe')

    def unpack(self):
        # We download directly the exe file so we copy it on the tool directory ...
        self.mark_deps = extract_exec(self.archive_file, self.build_dir, check_file = self.full_exe, force_dest = self.full_exe, check_mark=True)

@tool_add
class Tool_go(Tool):
    def __init__(self):
        Tool.__init__(self,
            'go',
            archive_url = 'https://dl.google.com/go/go1.10.windows-amd64.zip',
            hash = '210b223031c254a6eb8fa138c3782b23af710a9959d64b551fa81edd762ea167',
            dir_part = 'go-1.10',
            )

    def load_defaults(self):
        Tool.load_defaults(self)
        self.tool_path = os.path.join(self.build_dir, 'bin')
        self.full_exe = os.path.join(self.tool_path, 'go.exe')

    def unpack(self):
        # We download directly the exe file so we copy it on the tool directory ...
        self.mark_deps = extract_exec(self.archive_file, self.build_dir, check_file = self.full_exe, check_mark=True, strip_one=True)
