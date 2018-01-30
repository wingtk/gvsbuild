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
from urllib.request import splittype, urlopen, ContentTooShortError
from urllib.error import URLError
import contextlib
import ssl
import zipfile
import re
import copy

from .utils import ordered_set
from .utils import rmtree_full
from .simple_ui import script_title
from .simple_ui import global_verbose, error_exit, print_debug, print_log, print_message
from .base_project import Project
from .base_expanders import dirlist2set
from .base_expanders import make_zip

class Builder(object):
    def __init__(self, opts):
        self.opts = opts

        script_title('* Setup')

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

        if opts.from_scratch:
            print('Removing working/building dir (%s)' % (self.working_dir, ))
            rmtree_full(self.working_dir, retry=True)
            print('Removing destination dir (%s)' % (self.gtk_dir, ))
            rmtree_full(self.gtk_dir, retry=True)
            if not opts.keep_tools:
                print('Removing tools dir (%s)' % (opts.tools_root_dir, ))
                rmtree_full(opts.tools_root_dir, retry=True)

        if not opts.use_env:
            self.__minimum_env()

        self.__check_tools(opts)
        self.__check_vs(opts)

        self.x86 = opts.platform == 'Win32'
        self.x64 = not self.x86

        self.msbuild_opts = '/nologo /p:Platform=%(platform)s /p:PythonPath="%(python_dir)s" /p:PythonDir="%(python_dir)s" %(msbuild_opts)s ' % \
            dict(platform=opts.platform, python_dir=opts.python_dir, configuration=opts.configuration, msbuild_opts=opts.msbuild_opts)

        if global_verbose:
            self.msbuild_opts += ' /v:normal'
        else:
            self.msbuild_opts += ' /v:minimal'

        # Create the year version for Visual studio
        vs_zip_parts = {
            '12': 'vs2013',
            '14': 'vs2015',
            '15': 'vs2017',
        }

        self.vs_ver_year = vs_zip_parts.get(opts.vs_ver, None)
        if not self.vs_ver_year:
            self.vs_ver_year = 'ms-cl-%s' % (opts.vs_ver, )

        vs_part = self.vs_ver_year
        if opts.win_sdk_ver:
            vs_part += '-' + opts.win_sdk_ver
            self.msbuild_opts += ' /p:WindowsTargetPlatformVersion="%s"' % (opts.win_sdk_ver, )

        self.zip_dir = os.path.join(opts.build_dir, 'dist', vs_part, opts.platform, opts.configuration)
        if opts.make_zip:
            if opts.zip_continue:
                self.file_built = self._load_built_files()
            else:
                # Remove the destination dir before starting anything
                if os.path.isdir(self.gtk_dir):
                    print_log('Removing build dir (%s)' % (self.gtk_dir, ))
                    rmtree_full(self.gtk_dir)
                self.file_built = set()
            os.makedirs(self.zip_dir, exist_ok=True)

    def __minimum_env(self):
        """
        Set the environment to the minimum needed to run, leaving only
        the c:\windows\XXXX directory and the git one.

        The LIB, LIBPATH & INCLUDE environment are also cleaned to avoid
        mismatch with  libs / programs already installed
        """

        print_debug('Cleaning up the build environment')
        win_dir = os.environ.get('SYSTEMROOT', r'c:\windows').lower()

        win_dir = win_dir.replace('\\', '\\\\')
        print_debug('windir -> %s' % (win_dir, ))

        chk_re = [
            re.compile('^%s\\\\' % (win_dir, )),
            re.compile('^%s$' % (win_dir, )),
            re.compile('\\\\git\\\\'),
            re.compile('\\\\git$'),
        ]

        mp = []
        paths = os.environ.get('PATH', '').split(';')
        for k in paths:
            # use all lower
            k = os.path.normpath(k).lower()
            if k in mp:
                # already present
                print_debug("   Already present: '%s'" % (k, ))
                continue

            add = False
            for cre in chk_re:
                if cre.search(k):
                    mp.append(k)
                    add = True
                    break
            if add:
                print_debug("Add '%s'" % (k, ))
            else:
                print_debug("   Skip '%s'" % (k, ))

        print_debug('Final path:')
        for i in mp:
            print_debug('    %s' % (i, ))
        os.environ['PATH'] = ';'.join(mp)

        os.environ['LIB'] = ''
        os.environ['LIBPATH'] = ''
        os.environ['INCLUDE'] = ''
        print_debug('End environment setup')

    def __msys_missing(self, base_dir):
        msys_pkg = [
            ('patch',      'patch'),
            ('make',       'make'),
            ('md5sum',     'coreutils'),
            ('diff',       'diffutils'),
            ('bison',       'bison'),
        ]
        missing = []
        for prog, pkg in msys_pkg:
            if not os.path.isfile(os.path.join(base_dir, 'usr', 'bin', prog + '.exe')):
                print_log('msys: missing package %s' % (pkg, ))
                missing.append(pkg)
        return missing

    def __check_tools(self, opts):
        script_title('* Msys tool')
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

    def _add_env(self, key, value, env, prepend=True, subst=False):
        # env manipulation helper fun
        # returns a tuple with the old (key, value, ) to let the script restore it if needed
        org_env = env.get(key, None)
        if subst:
            te = None
        else:
            te = org_env
        if te:
            if prepend:
                env[key] = value + ';' + te
            else:
                env[key] = te + ';' + value
        else:
            # not set or forced
            env[key] = value
        return (key, org_env, )

    def add_global_env(self, key, value, prepend=True):
        # Env to load before the setup for the visual studio environment
        self._add_env(key, value, os.environ, prepend)

    def mod_env(self, key, value, prepend=True, subst=False):
        # Modify the current build environment
        # returns the old value
        return self._add_env(key, value, self.vs_env, prepend=prepend, subst=subst)

    def restore_env(self, saved):
        if saved:
            key, value = saved
            if key:
                if value:
                    self.vs_env[key] = value
                else:
                    del self.vs_env[key]
            
    def __check_vs(self, opts):
        script_title('* Msvc tool')
        # Verify VS exists at the indicated location, and that it supports the required target
        add_opts = ''
        if opts.platform == 'Win32':
            vcvars_bat = os.path.join(opts.vs_install_path, 'VC', 'bin', 'vcvars32.bat')
            # make sure it works with VS 2017
            if not os.path.exists(vcvars_bat):
                vcvars_bat=os.path.join(opts.vs_install_path, 'VC', 'Auxiliary', 'Build', 'vcvars32.bat')
            if opts.win_sdk_ver:
                add_opts = ' %s' % (opts.win_sdk_ver, )
        else:
            vcvars_bat = os.path.join(opts.vs_install_path, 'VC', 'bin', 'amd64', 'vcvars64.bat')
            # make sure it works with VS Express
            if not os.path.exists(vcvars_bat):
                vcvars_bat = os.path.join(opts.vs_install_path, 'VC', 'bin', 'x86_amd64', 'vcvarsx86_amd64.bat')
            # make sure it works with VS 2017
            if not os.path.exists(vcvars_bat):
                vcvars_bat=os.path.join(opts.vs_install_path, 'VC', 'Auxiliary', 'Build', 'vcvars64.bat')
            if opts.win_sdk_ver:
                add_opts = ' %s' % (opts.win_sdk_ver, )

        if not os.path.exists(vcvars_bat):
            raise Exception("'%s' could not be found. Please check you have Visual Studio installed at '%s' and that it supports the target platform '%s'." % (vcvars_bat, opts.vs_install_path, opts.platform))

        # Add to the environment the gtk paths so meson can find everything
        self.add_global_env('INCLUDE', os.path.join(self.gtk_dir, 'include'))
        self.add_global_env('LIB', os.path.join(self.gtk_dir, 'lib'))
        self.add_global_env('LIBPATH', os.path.join(self.gtk_dir, 'lib'))
        self.add_global_env('PATH', os.path.join(self.gtk_dir, 'bin'))

        output = subprocess.check_output('cmd.exe /c ""%s"%s>NUL && set"' % (vcvars_bat, add_opts, ), shell=True)
        self.vs_env = {}
        for l in output.splitlines():
            # python 3 str is not bytes and no need to decode
            k, v = (l.decode('utf-8') if isinstance(l, bytes) else l).split("=", 1)
            # Be sure to have PATH in upper case because we need to manipulate it
            if k.upper() == 'PATH':
                k = 'PATH'
            self.vs_env[k] = v
            print_debug('vs env:%s -> [%s]' % (k, v, ))

    def preprocess(self):
        for proj in Project.list_projects():
            if proj.archive_url:
                if proj.archive_file_name:
                    archive = proj.archive_file_name
                else:
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
        script_title(None)

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

        script_title('* Downloading')
        for p in projects:
            if self.__download_one(p):
                return True
        return False

    def _load_built_files(self):
        """
        Return a set with all the files present in the final, installation, dir
        """
        return dirlist2set(self.gtk_dir)

    def __build_one(self, proj):
        if self.opts.fast_build and not self.opts.clean:
            if os.path.isdir(proj.build_dir):
                print_message("Fast build:skipping project %s" % (proj.name, ))
                return 
            
        print_message("Building project %s" % (proj.name,))
        script_title(proj.name)

        # save the vs environment
        saved_env = copy.copy(self.vs_env)
        proj.builder = self
        self.__project = proj

        proj.prepare_build_dir()

        proj.pkg_dir = proj.build_dir + "-rel"
        shutil.rmtree(proj.pkg_dir, ignore_errors=True)
        os.makedirs(proj.pkg_dir)

        # Get the paths to add
        paths = self.vs_env['PATH'].split(';')
        # Add the paths needed
        for d in proj.all_dependencies:
            t = d.get_path()
            if t:
                if isinstance(t, tuple):
                    # pre/post
                    if t[0]:
                        # Add at the beginning,
                        paths.insert(0, t[0])
                    if t[1]:
                        # Add at the end (msys, )
                        paths.append(t[1])
                else:
                    # Single path,  at the beginning
                    paths.insert(0, t)

        # Make the (eventually) new path
        self.vs_env['PATH'] = ';'.join(paths)

        proj.patch()
        proj.build()

        print_debug("copying %s to %s" % (proj.pkg_dir, self.gtk_dir))
        self.copy_all(proj.pkg_dir, self.gtk_dir)
        shutil.rmtree(proj.pkg_dir, ignore_errors=True)

        proj.post_install()

        proj.builder = None
        self.__project = None
        # Restore the full environment
        self.vs_env = saved_env
        saved_env = None

        if self.opts.make_zip:
            # Create file list
            cur = self._load_built_files()
            # delta with the old
            new = cur - self.file_built
            if new:
                # file presents, do the zip
                zip_file = os.path.join(self.zip_dir, proj.name + '.zip')
                self.make_zip(zip_file, new)
                # use the current file set
                self.file_built = cur
            else:
                # No file preentt
                print_log("%s:zip not needed (tool?)" % (proj.name, ))
        script_title(None)

    def make_zip(self, name, files):
        make_zip(name, files, skip_spc=len(self.gtk_dir))

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

    def urlretrieve(self, url, filename, reporthook, ssl_ignore_cert=False):
        """
        Retrieve a URL into a temporary location on disk.

        Requires a URL argument. If a filename is passed, it is used as
        the temporary file location. The reporthook argument should be
        a callable that accepts a block number, a read size, and the
        total file size of the URL target. The data argument should be
        valid URL encoded data.

        If a filename is passed and the URL points to a local resource,
        the result is a copy from local file to new file.

        Returns a tuple containing the path to the newly created
        data file as well as the resulting HTTPMessage object.
        """
        url_type, path = splittype(url)

        if ssl_ignore_cert:
            # ignore certificate
            ssl_ctx = ssl._create_unverified_context()
        else:
            # let the library does the work
            ssl_ctx = None

        msg = 'Opening %s ...' % (url, )
        print(msg, end='\r')
        with contextlib.closing(urlopen(url, None, context=ssl_ctx)) as fp:
            print('%*s' % (len(msg), '', ), end = '\r')
            headers = fp.info()

            with open(filename, 'wb') as tfp:
                result = filename, headers
                bs = 1024*8
                size = -1
                read = 0
                blocknum = 0
                if "content-length" in headers:
                    size = int(headers["Content-Length"])

                reporthook(blocknum, bs, size)

                while True:
                    block = fp.read(bs)
                    if not block:
                        break
                    read += len(block)
                    tfp.write(block)
                    blocknum += 1
                    reporthook(blocknum, bs, size)

        if size >= 0 and read < size:
            raise ContentTooShortError(
                "retrieval incomplete: got only %i out of %i bytes"
                % (read, size), result)

        return result

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
        try:
            self.urlretrieve(proj.archive_url, proj.archive_file, self.__download_progress)
        except (ssl.SSLError, URLError) as e:
            print("Exception downloading file '%s'" % (proj.archive_url, ))
            print(e)
            if hasattr(proj, 'hash'):
                self._old_perc = -1
                self._old_print = 0
                self.urlretrieve(proj.archive_url, proj.archive_file, self.__download_progress, ssl_ignore_cert=True)
            else:
                print('Hash not present, bailing out ;(')
                raise

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
        if key:
            env[key] = env[key] + ';' + folder
        else:
            key = 'path'
            env[key] = folder
        print_debug("Changed path env variable to '%s'" % env[key])
