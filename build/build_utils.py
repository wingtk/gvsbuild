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

# Base building fun / classes, utility fun & var

import os
import shutil
import stat
import sys

global_verbose = False
global_debug = False

def print_message(msg):
    print(msg)

def print_log(msg):
    if global_verbose:
        print(msg)

def print_debug(msg):
    if global_debug:
        print("Debug:", msg)

def error_exit(msg):
    print("Error:", msg, file=sys.stderr)
    sys.exit(1)

def convert_to_msys(path):
    path = path
    if path[1] != ':':
        raise Exception('oops')
    path = '/' + path[0] + path[2:].replace('\\', '/')
    return path

def _rmtree_error_handler(func, path, exc_info):
    if not os.access(path, os.W_OK):
        # Is the error an access error ?
        os.chmod(path, stat.S_IWUSR)
        func(path)
        print_debug('rmtree:read-only file/path (%s)' % (path, ))
    else:
        raise

class ordered_set(set):
    def __init__(self):
        set.__init__(self)
        self.__list = list()

    def add(self, o):
        if not o in self:
            set.add(self, o)
            self.__list.append(o)

    def __iter__(self):
        return self.__list.__iter__()

class Tarball(object):
    def unpack(self):
        print_log('Extracting %s to %s' % (self.archive_file, self.builder.working_dir))

        os.makedirs(self.build_dir)
        self.builder.exec_msys([self.builder.tar, 'ixf', convert_to_msys(self.archive_file), '-C', convert_to_msys(self.build_dir), '' if self.tarbomb else '--strip-components=1'])

        print_log('Extracted %s' % (self.archive_file,))

class MercurialRepo(object):
    def unpack(self):
        print_log('Cloning %s to %s' % (self.repo_url, self.build_dir))
        self.exec_cmd('hg clone %s %s-tmp' % (self.repo_url, self.build_dir))
        shutil.move(self.build_dir + '-tmp', self.build_dir)
        print_log('Cloned %s to %s' % (self.repo_url, self.build_dir))

    def update_build_dir(self):
        print_log('Updating directory %s' % (self.build_dir,))
        self.exec_cmd('hg pull -u', working_dir=self.build_dir)

class GitRepo(object):
    def unpack(self):
        print_log('Cloning %s to %s' % (self.repo_url, self.build_dir))

        self.builder.exec_msys('git clone %s %s-tmp' % (self.repo_url, self.build_dir))
        shutil.move(self.build_dir + '-tmp', self.build_dir)

        if self.fetch_submodules:
            self.builder.exec_msys('git submodule update --init',  working_dir=self.build_dir)

        if self.tag:
            self.builder.exec_msys('git checkout -f %s' % self.tag, working_dir=self.build_dir)

        print_log('Cloned %s to %s' % (self.repo_url, self.build_dir))

    def update_build_dir(self):
        print_log('Updating directory %s' % (self.build_dir,))

        # I don't like too much this, but at least we ensured it is properly cleaned up
        self.builder.exec_msys('git clean -xdf', working_dir=self.build_dir)

        if self.tag:
            self.builder.exec_msys('git fetch origin', working_dir=self.build_dir)
            self.builder.exec_msys('git checkout -f %s' % self.tag, working_dir=self.build_dir)
        else:
            self.builder.exec_msys('git checkout -f', working_dir=self.build_dir)
            self.builder.exec_msys('git pull --rebase', working_dir=self.build_dir)

        if self.fetch_submodules:
            self.builder.exec_msys('git submodule update --init', working_dir=self.build_dir)

        if os.path.exists(self.patch_dir):
            print_log("Copying files from %s to %s" % (self.patch_dir, self.build_dir))
            self.builder.copy_all(self.patch_dir, self.build_dir)

class Project(object):
    def __init__(self, name, **kwargs):
        object.__init__(self)
        self.name = name
        self.dependencies = []
        self.patches = []
        self.archive_url = None
        self.tarbomb = False
        for k in kwargs:
            setattr(self, k, kwargs[k])
        self.__working_dir = None

    _projects = []
    _names = []
    _dict = {}

    def __str__(self):
        return self.name

    def __repr__(self):
        return repr(self.name)

    def load_defaults(self, builder):
        # Used by the tools to load default paths/filenames
        pass

    def build(self):
        raise NotImplementedError('build')

    def post_install(self):
        pass

    def exec_cmd(self, cmd, working_dir=None, add_path=None):
        self.builder.exec_cmd(cmd, working_dir=working_dir, add_path=add_path)

    def exec_vs(self, cmd, add_path=None):
        self.builder.exec_vs(cmd, working_dir=self._get_working_dir(), add_path=add_path)

    def exec_msbuild(self, cmd, configuration=None, add_path=None):
        if not configuration:
            configuration = '%(configuration)s'
        self.exec_vs('msbuild ' + cmd + ' /p:Configuration=' + configuration + ' %(msbuild_opts)s', add_path=add_path)

    def install(self, *args):
        self.builder.install(self._get_working_dir(), self.pkg_dir, *args)

    def install_dir(self, src, dest=None):
        if not dest:
            dest = os.path.basename(src)
        self.builder.install_dir(self._get_working_dir(), self.pkg_dir, src, dest)

    def patch(self):
        for p in self.patches:
            name = os.path.basename(p)
            stamp = os.path.join(self.build_dir, name + ".patch-applied")
            if not os.path.exists(stamp):
                print_log("Applying patch %s" % (p,))
                self.builder.exec_msys(['patch', '-p1', '-i', p], working_dir=self._get_working_dir())
                with open(stamp, 'w') as stampfile:
                    stampfile.write('done')
            else:
                print_debug("patch %s already applied, skipping" % (p,))

    def _get_working_dir(self):
        if self.__working_dir:
            return os.path.join(self.build_dir, self.__working_dir)
        else:
            return self.build_dir

    def push_location(self, path):
        self.__working_dir = path

    def pop_location(self):
        self.__working_dir = None

    def prepare_build_dir(self):
        if self.builder.opts.clean and os.path.exists(self.build_dir):
            shutil.rmtree(self.build_dir, onerror=_rmtree_error_handler)

        if os.path.exists(self.build_dir):
            print_debug("directory %s already exists" % (self.build_dir,))
            self.update_build_dir()
        else:
            self.unpack()
            if os.path.exists(self.patch_dir):
                print_log("Copying files from %s to %s" % (self.patch_dir, self.build_dir))
                self.builder.copy_all(self.patch_dir, self.build_dir)

    def update_build_dir(self):
        pass

    def unpack(self):
        raise NotImplementedError("unpack")

    def get_path(self):
        # Optional for projects
        pass

    @staticmethod
    def add(proj):
        if proj.name in Project._dict:
            error_exit("Project '%s' alreaady present!" % (proj.name, )) 
        Project._projects.append(proj)
        Project._names.append(proj.name)
        Project._dict[proj.name] = proj

    @staticmethod
    def get_project(name):
        return Project._dict[name]

    @staticmethod
    def list_projects():
        return list(Project._projects)

    @staticmethod
    def get_names():
        return list(Project._names)

    @staticmethod
    def get_dict():
        return dict(Project._dict)

class CmakeProject(Tarball, Project):
    def __init__(self, name, **kwargs):
        Project.__init__(self, name, **kwargs)

    def build(self):
        cmake_config = 'Debug' if self.builder.opts.configuration == 'debug' else 'RelWithDebInfo'
        self.exec_vs('cmake -G "NMake Makefiles" -DCMAKE_INSTALL_PREFIX="%(pkg_dir)s" -DGTK_DIR="%(gtk_dir)s" -DCMAKE_BUILD_TYPE=' + cmake_config)
        self.exec_vs('nmake /nologo')
        self.exec_vs('nmake /nologo install')

class MercurialCmakeProject(MercurialRepo, CmakeProject):
    def __init__(self, name, **kwargs):
        CmakeProject.__init__(self, name, **kwargs)

class Meson(Project):
    def __init__(self, name, **kwargs):
        Project.__init__(self, name, **kwargs)

    def build(self, meson_params=None):
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
        # we simply run 'ninja install' that takes care of everything, running explicity from the build dir
        self.builder.exec_vs('ninja install', working_dir=ninja_build)

class Tool(Project):
    def __init__(self, name, **kwargs):
        self.dir_part = None
        Project.__init__(self, name, **kwargs)

    def load_defaults(self, builder):
        if self.dir_part:
            self.build_dir = os.path.join(builder.opts.tools_root_dir, self.dir_part)
        else:
            self.build_dir = os.path.join(builder.opts.tools_root_dir, self.name)

    def build(self):
        # All the work is done in the unpack
        pass

    def get_path(self):
        # Mandatory for tools
        raise NotImplementedError("get_path")
