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
Main builder class
"""

import os
import shutil
import subprocess
import traceback
import glob
import hashlib
import urllib.request

from .utils import ordered_set
from .simple_ui import global_verbose, error_exit, print_debug, print_log, print_message
from .base_project import Project

class Builder(object):
    def __init__(self, opts):
        self.opts = opts

        # Check and normalize the platform
        if opts.platform in ('Win32', 'win32', 'x86'):
            opts.platform = 'Win32'
            self.filename_arch = 'x86'
        elif opts.platform in ('x64', 'amd64', 'Amd64'):
            opts.platform = 'x64'
            self.filename_arch = 'x64'
        else:
            raise Exception("Invalid target platform '%s'" % (opts.platform,))

        # Setup the directory, used by check vs
        self.working_dir = os.path.join(opts.build_dir, 'build', opts.platform, opts.configuration)
        self.gtk_dir = os.path.join(opts.build_dir, 'gtk', opts.platform, opts.configuration)

        self.__check_tools(opts)
        self.__check_vs(opts)

        self.x86 = opts.platform == 'Win32'
        self.x64 = not self.x86

        self.msbuild_opts = '/nologo /p:Platform=%(platform)s /p:PythonPath=%(python_dir)s %(msbuild_opts)s ' % \
            dict(platform=opts.platform, python_dir=opts.python_dir, configuration=opts.configuration, msbuild_opts=opts.msbuild_opts)

        if global_verbose:
            self.msbuild_opts += ' /v:normal'
        else:
            self.msbuild_opts += ' /v:minimal'

    def __msys_missing(self, base_dir):
        msys_pkg = [ ('nasm',       'nasm'),
                     ('patch',      'patch'),
                     ('msgfmt',     'gettext'),
                     ('make',       'make'),
                     ('md5sum',     'coreutils'),
                     ('diff',       'diffutils'),
                     ('pkg-config', 'pkg-config'),
                     ]
        missing = []
        for prog, pkg in msys_pkg:
            if not os.path.isfile(os.path.join(base_dir, 'usr', 'bin', prog + '.exe')):
                print_log('msys: missing package %s' % (pkg, )) 
                missing.append(pkg)
        return missing

    def __check_tools(self, opts):
        # what's missing ?
        missing = self.__msys_missing(opts.msys_dir) 
        if missing:
            # install using pacman 
            cmd = os.path.join(opts.msys_dir, 'usr', 'bin', 'bash') + ' -l -c "pacman --noconfirm -S ' + ' '.join(missing) + '"'
            print_debug("Updating msys2 with '%s'" % (cmd, ))
            subprocess.check_call(cmd, shell=True)
            missing = self.__msys_missing(opts.msys_dir)
            if missing:
                # oops
                cmd = 'pacman -S ' + ' '.join(missing)
                error_exit("Missing package(s) from msys2 installation, try with\n    '%s'\nin a msys2 shell." % (cmd, ))

        self.patch = os.path.join(opts.msys_dir, 'usr', 'bin', 'patch.exe')
        if not os.path.exists(self.patch):
            error_exit("%s not found. Please check that you installed patch in msys2 using ``pacman -S patch``" % (self.patch,))
        print_debug("patch: %s" % (self.patch,))

        self.msgfmt = os.path.join(opts.msys_dir, 'usr', 'bin', 'msgfmt.exe')
        if not os.path.exists(self.msgfmt):
            error_exit("%s not found. Please check that you installed msgfmt in msys2 using ``pacman -S gettext``" % (self.msgfmt,))
        print_debug("msgfmt: %s" % (self.msgfmt,))

    def add_env(self, key, value, prepend=True):
        env = os.environ
        te = env.get(key, None)
        if te:
            if prepend:
                env[key] = value + ';' + te
            else:
                env[key] = te + ';' + value
        else:
            # not set
            env[key] = value

    def __check_vs(self, opts):
        # Verify VS exists at the indicated location, and that it supports the required target
        if opts.platform == 'Win32':
            vcvars_bat = os.path.join(opts.vs_install_path, 'VC', 'bin', 'vcvars32.bat')
        else:
            vcvars_bat = os.path.join(opts.vs_install_path, 'VC', 'bin', 'amd64', 'vcvars64.bat')
            # make sure it works even with VS Express
            if not os.path.exists(vcvars_bat):
                vcvars_bat = os.path.join(opts.vs_install_path, 'VC', 'bin', 'x86_amd64', 'vcvarsx86_amd64.bat')

        if not os.path.exists(vcvars_bat):
            raise Exception("'%s' could not be found. Please check you have Visual Studio installed at '%s' and that it supports the target platform '%s'." % (vcvars_bat, opts.vs_install_path, opts.platform))

        # Add to the environment the gtk paths so meson can find everything
        self.add_env('INCLUDE', os.path.join(self.gtk_dir, 'include'))
        self.add_env('LIB', os.path.join(self.gtk_dir, 'lib'))
        self.add_env('LIBPATH', os.path.join(self.gtk_dir, 'lib'))
        self.add_env('PATH', os.path.join(self.gtk_dir, 'bin'))

        output = subprocess.check_output('cmd.exe /c ""%s" && set"' % (vcvars_bat,), shell=True)
        self.vs_env = {}
        for l in output.splitlines():
            k, v = l.decode('utf-8').split("=", 1)
            # Be sure to have PATH in upper case because we need to manipulate it
            if k.upper() == 'PATH':
                k = 'PATH'
            self.vs_env[k] = v
            print_debug('vs env:%s -> [%s]' % (k, v, ))

    def preprocess(self):
        for proj in Project.list_projects():
            if proj.archive_url:
                url = proj.archive_url
                archive = url[url.rfind('/') + 1:]
                proj.archive_file = os.path.join(self.opts.archives_download_dir, archive)
            else:
                proj.archive_file = None
            proj.patch_dir = os.path.join(self.opts.patches_root_dir, proj.name)
            proj.build_dir = os.path.join(self.working_dir, proj.name)
            proj.dependencies = [Project.get_project(dep) for dep in proj.dependencies]
            proj.dependents = []
            proj.load_defaults(self)

        for proj in Project.list_projects():
            self.__compute_deps(proj)
            print_debug("%s => %s" % (proj.name, [d.name for d in proj.all_dependencies]))

    def __compute_deps(self, proj):
        if hasattr(proj, 'all_dependencies'):
            return
        deps = ordered_set()
        for dep in proj.dependencies:
            self.__compute_deps(dep)
            for p in dep.all_dependencies:
                deps.add(p)
            deps.add(dep)
        proj.all_dependencies = deps

    def build(self, projects):
        if self.__prepare_build(projects):
            return

        if self.opts.check_hash:
            return

        for p in projects:
            try:
                self.__build_one(p)
            except:
                traceback.print_exc()
                error_exit("%s build failed" % (p.name))

    def __prepare_build(self, projects):
        if not os.path.exists(self.working_dir):
            print_log("Creating working directory %s" % (self.working_dir,))
            os.makedirs(self.working_dir)

        shutil.copy(os.path.join(self.opts.patches_root_dir, 'stack.props'), self.working_dir)

        log_dir = os.path.join(self.working_dir, 'logs')
        if not os.path.exists(log_dir):
            print_log("Creating log directory %s" % (log_dir,))
            os.makedirs(log_dir)

        #Remove-Item $logDirectory\*.log

        build_dir = os.path.join(self.working_dir, '..', '..', '..', 'gtk', self.opts.platform)
        if not os.path.exists(build_dir):
            print_log("Creating directory %s" % (build_dir,))
            os.makedirs(build_dir)

        for p in projects:
            if self.__download_one(p):
                return True
        return False

    def __build_one(self, proj):
        print_message("Building project %s" % (proj.name,))

        proj.builder = self
        self.__project = proj

        proj.prepare_build_dir()

        proj.pkg_dir = proj.build_dir + "-rel"
        shutil.rmtree(proj.pkg_dir, ignore_errors=True)
        os.makedirs(proj.pkg_dir)

        # Get the paths to add
        paths = []
        for d in proj.all_dependencies:
            t = d.get_path()
            if t:
                paths.append(t)

        # Save base vs path
        vs_saved_path = self.vs_env['PATH']
        if paths:
            # Something to add to the vs environment path, at the beginning
            tp = ';'.join(paths)
            self.vs_env['PATH'] = tp + ';' + vs_saved_path

        proj.patch()
        proj.build()

        print_debug("copying %s to %s" % (proj.pkg_dir, self.gtk_dir))
        self.copy_all(proj.pkg_dir, self.gtk_dir)
        shutil.rmtree(proj.pkg_dir, ignore_errors=True)

        proj.post_install()

        proj.builder = None
        self.__project = None
        if vs_saved_path:
            # Restore the original vs path
            self.vs_env['PATH'] = vs_saved_path

    def make_dir(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    def copy_all(self, srcdir, destdir):
        self.make_dir(destdir)
        for f in glob.glob('%s\\*' % (srcdir,)):
            self.__copy_to(f, destdir)

    def __copy_to(self, src, destdir):
        #print_debug("__copy_to %s %s" % (src, destdir))
        self.make_dir(destdir)
        for f in glob.glob(src):
            if os.path.isdir(f):
                name = os.path.basename(f)
                dest_subdir = os.path.join(destdir, name)
                self.make_dir(dest_subdir)
                for item in os.listdir(f):
                    self.__copy_to(os.path.join(f, item), dest_subdir)
            else:
                shutil.copy2(f, destdir)

    def __copy(self, src, destdir):
        if os.path.isdir(src):
            dst = os.path.join(destdir, os.path.basename(src))
            print_debug("copying '%s' to '%s'" % (src, dst))
            shutil.copytree(src, dst)
        else:
            print_debug("copying '%s' to '%s'" % (src, destdir))
            shutil.copy(src, destdir)

    def __hashfile(self, file_name):
        hash_calc = hashlib.sha256()
        with open(file_name, 'rb') as fi:
            for chunk in iter(lambda: fi.read(4096), b""):
                hash_calc.update(chunk)
        return hash_calc.hexdigest()

    def __check_hash(self, proj):
        if hasattr(proj, 'hash'):
            hc = self.__hashfile(proj.archive_file)
            if hc != proj.hash:
                print_message("Hash mismatch on %s:\n  Calculated '%s'\n  Expected   '%s'\n" % (proj.archive_file, hc, proj.hash, ))
                return True

            # Print the correct hash
            if self.opts.check_hash:
                print_message("Hash ok on %s (%s)" % (proj.archive_file, hc, ))
            else:
                print_debug("Hash ok on %s (%s)" % (proj.archive_file, hc, ))
        return False

    def __download_progress(self, count, block_size, total_size):
        c_size = count * block_size
        if total_size > 0:
            # Percentage
            perc = (100 * c_size) // total_size
            if perc != self._old_perc:
                if perc > 100:
                    perc = 100
                self._old_perc = perc
                sp = '%s (%u k) - %u%%' % (self._downloading_file, total_size / 1024, self._old_perc, )
                print(sp, end='\r')
                if len(sp) > self._old_print:
                    # Save the len to delete the line when we change file
                    self._old_print = len(sp)
        else:
            # Only the current, we don't know the size
            sp = '%s - %u k' % (self._downloading_file, c_size / 1024, )
            print(sp, end='\r')
            if len(sp) > self._old_print:
                self._old_print = len(sp)

    def __download_one(self, proj):
        if not proj.archive_file:
            print_debug("archive file is not specified for project %s, skipping" % (proj.name,))
            return False

        if os.path.exists(proj.archive_file):
            print_debug("archive %s already exists" % (proj.archive_file,))
            return self.__check_hash(proj)

        if not os.path.exists(self.opts.archives_download_dir):
            print_log("Creating archives download directory %s" % (self.opts.archives_download_dir,))
            os.makedirs(self.opts.archives_download_dir)

        print_log("downloading %s" % (proj.archive_file,))
        # Setup for progress show
        self._downloading_file = proj.archive_file
        self._old_perc = -1
        self._old_print = 0
        urllib.request.urlretrieve(proj.archive_url, proj.archive_file, reporthook=self.__download_progress)
        print('%-*s' % (self._old_print, '%s - Download finished' % (proj.archive_file, )), )
        return self.__check_hash(proj)

    def __sub_vars(self, s):
        if '%' in s:
            d = dict(platform=self.opts.platform, configuration=self.opts.configuration, build_dir=self.opts.build_dir, vs_ver=self.opts.vs_ver,
                     gtk_dir=self.gtk_dir, python_dir=self.opts.python_dir, perl_dir=self.perl_dir, msbuild_opts=self.msbuild_opts)
            if self.__project is not None:
                d['pkg_dir'] = self.__project.pkg_dir
                d['build_dir'] = self.__project.build_dir
            return s % d
        else:
            return s

    def exec_vs(self, cmd, working_dir=None, add_path=None):
        self.__execute(self.__sub_vars(cmd), working_dir=working_dir, add_path=add_path, env=self.vs_env)

    def exec_cmd(self, cmd, working_dir=None, add_path=None):
        self.__execute(self.__sub_vars(cmd), working_dir=working_dir, add_path=add_path)

    def install(self, build_dir, pkg_dir, *args):
        if len(args) == 1:
            args = args[0].split()
        dest = os.path.join(pkg_dir, self.__sub_vars(args[-1]))
        self.make_dir(dest)
        for f in args[:-1]:
            src = os.path.join(self.__sub_vars(build_dir), self.__sub_vars(f))
            print_debug("copying %s to %s" % (src, dest))
            self.__copy_to(src, dest)

    def install_dir(self, build_dir, pkg_dir, src, dest):
        src = os.path.join(build_dir, self.__sub_vars(src))
        dest = os.path.join(pkg_dir, self.__sub_vars(dest))
        print_debug("copying %s content to %s" % (src, dest))
        self.copy_all(src, dest)

    def exec_msys(self, args, working_dir=None):
        self.__execute(args, working_dir=working_dir, add_path=os.path.join(self.opts.msys_dir, 'usr', 'bin'))

    def __execute(self, args, working_dir=None, add_path=None, env=None):
        print_debug("running %s, cwd=%s, path+=%s" % (args, working_dir, add_path))
        if add_path:
            if env is not None:
                env = dict(env)
            else:
                env = dict(os.environ)
            self.__add_path(env, add_path)
        subprocess.check_call(args, cwd=working_dir, env=env, shell=True)

    def __add_path(self, env, folder):
        key = None
        for k in env:
            if k.lower() == 'path':
                key = k
                break
        env[key] = env[key] + ';' + folder
