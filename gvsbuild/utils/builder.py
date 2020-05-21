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
from urllib.request import urlopen, ContentTooShortError
from urllib.error import URLError
import contextlib
import ssl
import re
import copy
import time
import json

from .utils import ordered_set
from .utils import rmtree_full
from .simple_ui import script_title
from .simple_ui import log
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
            opts.x86 = True
            self.filename_arch = 'x86'
        elif opts.platform in ('x64', 'amd64', 'Amd64'):
            opts.platform = 'x64'
            self.filename_arch = 'x64'
            opts.x86 = False
        else:
            raise Exception("Invalid target platform '%s'" % (opts.platform,))

        opts.x64 = not opts.x86
        # Setup the directory, used by check vs
        self.working_dir = os.path.join(opts.build_dir, 'build', opts.platform, opts.configuration)
        self.gtk_dir = os.path.join(opts.build_dir, 'gtk', opts.platform, opts.configuration)

        if opts.from_scratch:
            with log.simple_oper('Cleanup build directories'):
                with log.simple_oper('Removing working/building dir (%s)' % (self.working_dir, )):
                    rmtree_full(self.working_dir, retry=True)
                with log.simple_oper('Removing destination dir (%s)' % (self.gtk_dir, )):
                    rmtree_full(self.gtk_dir, retry=True)
                with log.simple_oper('Removing git expand dir (%s)' % (self.opts.git_expand_dir, )):
                    rmtree_full(self.opts.git_expand_dir, retry=True)
                if not opts.keep_tools:
                    with log.simple_oper('Removing tools dir (%s)' % (opts.tools_root_dir, )):
                        rmtree_full(opts.tools_root_dir, retry=True)
                else:
                    log.message('Keeping tools dir (%s)' % (opts.tools_root_dir, ))

        if not opts.use_env:
            self.__minimum_env()

        self.__check_tools(opts)
        self.__check_vs(opts)

        self.x86 = opts.platform == 'Win32'
        self.x64 = not self.x86

        # Create the year version for Visual studio
        vs_zip_parts = {
            '12': 'vs2013',
            '14': 'vs2015',
            '15': 'vs2017',
            '16': 'vs2019',
        }

        self.vs_ver_year = vs_zip_parts.get(opts.vs_ver, None)
        if not self.vs_ver_year:
            self.vs_ver_year = 'ms-cl-%s' % (opts.vs_ver, )

        vs_part = self.vs_ver_year
        if opts.win_sdk_ver:
            vs_part += '-' + opts.win_sdk_ver

        self.zip_dir = os.path.join(opts.build_dir, 'dist', vs_part, opts.platform, opts.configuration)
        if opts.make_zip:
            if opts.zip_continue:
                self.file_built = self._load_built_files()
            else:
                # Remove the destination dir before starting anything
                if os.path.isdir(self.gtk_dir):
                    with log.simple_oper('Removing build dir (%s)' % (self.gtk_dir, )):
                        rmtree_full(self.gtk_dir, retry=True)
                self.file_built = set()
            os.makedirs(self.zip_dir, exist_ok=True)

    def _create_msbuild_opts(self, python):
        rt = []
        rt.append('/nologo /p:Platform=%s' % self.opts.platform)
        if python:
            rt.append('/p:PythonPath="%(python_dir)s" /p:PythonDir="%(python_dir)s"' % dict(python_dir=python))

        if log.verbose_on():
            rt.append('/v:normal')
        else:
            rt.append('/v:minimal')

        if self.opts.win_sdk_ver:
            rt.append('/p:WindowsTargetPlatformVersion="%s"' % (self.opts.win_sdk_ver, ))

        if self.opts.msbuild_opts:
            rt.append(self.opts.msbuild_opts)

        return ' '.join(rt)

    def __minimum_env(self):
        """
        Set the environment to the minimum needed to run, leaving only
        the c:\windows\XXXX directory and the git one.

        The LIB, LIBPATH & INCLUDE environment are also cleaned to avoid
        mismatch with  libs / programs already installed
        """

        log.start('Cleaning up the build environment')
        win_dir = os.environ.get('SYSTEMROOT', r'c:\windows').lower()

        win_dir = win_dir.replace('\\', '\\\\')
        log.debug('windir -> %s' % (win_dir, ))

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
                log.debug("   Already present: '%s'" % (k, ))
                continue

            add = False
            for cre in chk_re:
                if cre.search(k):
                    mp.append(k)
                    add = True
                    break
            if add:
                log.debug("Add '%s'" % (k, ))
            else:
                log.debug("   Skip '%s'" % (k, ))

        log.debug('Final path:')
        for i in mp:
            log.debug('    %s' % (i, ))
        os.environ['PATH'] = ';'.join(mp)

        os.environ['LIB'] = ''
        os.environ['LIBPATH'] = ''
        os.environ['INCLUDE'] = ''
        log.end()

    def __msys_missing(self, base_dir):
        msys_pkg = [
            ('patch',      'patch'),
            ('make',       'make'),
            ('md5sum',     'coreutils'),
            ('diff',       'diffutils'),
            ('bison',       'bison'),
            ('flex',       'flex'),
        ]
        missing = []
        for prog, pkg in msys_pkg:
            if not os.path.isfile(os.path.join(base_dir, 'usr', 'bin', prog + '.exe')):
                log.log('msys: missing package %s' % (pkg, ))
                missing.append(pkg)
        return missing

    def __check_tools(self, opts):
        script_title('* Msys tool')
        log.start('Checking msys tool')
        # what's missing ?
        missing = self.__msys_missing(opts.msys_dir)
        if missing:
            # install using pacman
            cmd = os.path.join(opts.msys_dir, 'usr', 'bin', 'bash') + ' -l -c "pacman --noconfirm -S ' + ' '.join(missing) + '"'
            log.debug("Updating msys2 with '%s'" % (cmd, ))
            subprocess.check_call(cmd, shell=True)
            missing = self.__msys_missing(opts.msys_dir)
            if missing:
                # oops
                cmd = 'pacman -S ' + ' '.join(missing)
                log.error_exit("Missing package(s) from msys2 installation, try with\n    '%s'\nin a msys2 shell." % (cmd, ))

        self.patch = os.path.join(opts.msys_dir, 'usr', 'bin', 'patch.exe')
        if not os.path.exists(self.patch):
            log.error_exit("%s not found. Please check that you installed patch in msys2 using ``pacman -S patch``" % (self.patch,))
        log.debug("patch: %s" % (self.patch,))

        if opts.python_dir:
            if not os.path.isfile(os.path.join(opts.python_dir, 'python.exe')):
                log.error_exit("Executable python.exe not found at '%s'" % (self.opts.python_dir, ))
        log.end()

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

    def __dump_vs_loc(self):
        """
        Using vswhere try to locate the vs installation path
        """
        vswhere = r'%s\Microsoft Visual Studio\Installer\vswhere.exe' % (os.environ.get('ProgramFiles(x86)', r'C:\Program Files (x86)'))
        log.log('Trying to find Visual Studio installations ...')
        if not os.path.exists(vswhere):
            log.log('Could not find vswhere executable (%s)' % (vswhere, ))
            return

        json_file = 'vs-found.json'
        if os.path.exists(json_file):
            os.remove(json_file)

        cmd = '"%s" -all -products * -format json >%s' % (vswhere, json_file, )
        self.exec_cmd(cmd)

        res = None
        try:
            with open(json_file, 'rt') as fi:
                res = json.load(fi)
        except Exception as e:
            log.log('Exception reading vswhere result file (%s)' % (e, ))

        if res:
            log.message('')
            log.message('Visual studio installation(s) found:')
            for i in res:
                disp = i.get('displayName', '?')
                path = i.get('installationPath', r'?:\?')
                log.message('    %s @ %s' % (disp, path, ))
            log.message('')

    def __check_vs_single(self, opts, vs_path, exit_missing=True):
        # Verify VS exists at the indicated location, and that it supports the required target
        add_opts = ''
        if opts.platform == 'Win32':
            vcvars_bat = os.path.join(vs_path, 'VC', 'bin', 'vcvars32.bat')
            # make sure it works with VS 2017+
            if not os.path.exists(vcvars_bat):
                vcvars_bat=os.path.join(vs_path, 'VC', 'Auxiliary', 'Build', 'vcvars32.bat')
        else:
            vcvars_bat = os.path.join(vs_path, 'VC', 'bin', 'amd64', 'vcvars64.bat')
            # make sure it works with VS Express
            if not os.path.exists(vcvars_bat):
                vcvars_bat = os.path.join(vs_path, 'VC', 'bin', 'x86_amd64', 'vcvarsx86_amd64.bat')
            # make sure it works with VS 2017+
            if not os.path.exists(vcvars_bat):
                vcvars_bat=os.path.join(vs_path, 'VC', 'Auxiliary', 'Build', 'vcvars64.bat')

        if opts.win_sdk_ver:
            add_opts = ' %s' % (opts.win_sdk_ver, )

        log.log('Running script "%s"%s' % (vcvars_bat, add_opts, ))
        if not os.path.exists(vcvars_bat):
            if exit_missing:
                self.__dump_vs_loc();
                log.error_exit("\n  '%s' could not be found.\n  Please check you have Visual Studio installed at '%s'\n  and that it supports the target platform '%s'." % (vcvars_bat, vs_path, opts.platform))
            else:
                return None

        output = subprocess.check_output('cmd.exe /c ""%s"%s>NUL && set"' % (vcvars_bat, add_opts, ), shell=True)
        return output

    def __check_vs(self, opts):
        script_title('* Msvc tool')
        log.start('Checking Msvc tool')

        # Add to the environment the gtk paths so meson can find everything
        self.add_global_env('INCLUDE', os.path.join(self.gtk_dir, 'include'))
        self.add_global_env('LIB', os.path.join(self.gtk_dir, 'lib'))
        self.add_global_env('LIBPATH', os.path.join(self.gtk_dir, 'lib'))
        self.add_global_env('PATH', os.path.join(self.gtk_dir, 'bin'))

        if opts._vs_path_auto:
            dir_parts = [
                'Professional',
                'BuildTools',
                'Enterprise',
                'Community',
                'Preview',
                ]
            log.log('Looking for the Visual Studio version installed under %s ...' % (opts.vs_install_path, ))
            for part in dir_parts:
                output = self.__check_vs_single(opts, os.path.join(opts.vs_install_path, part), False)
                if output:
                    log.log("Found '%s'" % (part, ))
                    break

            if not output:
                # Nothing found, see what's installed & exit
                self.__dump_vs_loc();
                log.error_exit("\n  Visual Studio startup batch could not be found.\n  Please check you have Visual Studio installed under '%s\\[Professional|BuildTools|Community|...]'\n  and that it supports the target platform '%s'." % (opts.vs_install_path, opts.platform, ))
        else:
            output = self.__check_vs_single(opts, opts.vs_install_path, True)

        self.vs_env = {}
        dbg = log.debug_on()
        for l in output.splitlines():
            # Python3 str is not bytes and no need to decode
            l = l.decode('utf-8') if isinstance(l, bytes) else l
            e = l.split("=", 1)
            if len(e) < 2:
                log.debug('vs env: ignoring %s' % (l))
                continue
            k, v = e
            # Be sure to have PATH in upper case because we need to manipulate it
            if k.upper() == 'PATH':
                k = 'PATH'
            self.vs_env[k] = v
            if dbg:
                vl = v.split(';')
                if len(vl) > 1:
                    log.debug('vs env: %s: [' % (k, ))
                    for i in vl:
                        log.message_indent('  ' + i)
                    log.message_indent(']')
                else:
                    log.debug('vs env:%s -> [%s]' % (k, v, ))

        if not opts.win_sdk_ver:
            # Try lo figure the sdk version to pass it to the msbuild programs
            sdk = self.vs_env.get('WindowsSDKVersion', '')
            if not sdk or sdk == '\\':
                sdk = self.vs_env.get('WindowsSDKLibVersion', '')
            if sdk:
                # drop the last '\'
                if sdk[-1] == '\\':
                    sdk = sdk[:-1]
                if sdk == 'winv6.3':
                    sdk = '8.1'
                opts.win_sdk_ver = sdk
                log.log("Auto load win_sdk_ver: '%s'" % (sdk, ))

        log.end()

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
            proj.patch_dir = os.path.join(self.opts.patches_root_dir, proj.prj_dir)
            proj.build_dir = os.path.join(self.working_dir, proj.prj_dir)
            proj.dependencies = [Project.get_project(dep) for dep in proj.dependencies]
            proj.dependents = []
            proj.load_defaults()
            proj.mark_file_calc()
            if self.opts.clean:
                proj.clean = True

        for proj in Project.list_projects():
            self.__compute_deps(proj)
            log.debug("%s => %s" % (proj.name, [d.name for d in proj.all_dependencies]))

    def __compute_deps(self, proj):
        if hasattr(proj, 'all_dependencies'):
            return
        deps = ordered_set()
        for dep in proj.dependencies:
            self.__compute_deps(dep)
            for p in dep.all_dependencies:
                deps.add(p)
            deps.add(dep)
        proj.finalize_dep(self, deps)
        proj.all_dependencies = deps

    def _drop_proj(self, drop_prj):
        """
        Delete drop_prj and all the ones that depends on this from the list of projects to build
        """
        drop_list = [ drop_prj, ]
        while drop_list:
            drop_prj = drop_list.pop(0)

            print('* Removing %s dependents ...' % (drop_prj.name, ))
            for p in self.projects_to_do:
                if drop_prj in p.all_dependencies:
                    print("* > Removing %s for %s ..." % (p.name, drop_prj.name, ))
                    # Recursive drop
                    drop_list.append(p)
                    self.projects_to_do.remove(p)
                    self.prj_dropped.append(p.name)

    def build(self, projects):
        if self.__prepare_build(projects):
            return

        if self.opts.check_hash:
            return

        # List of all the project we can mark for build because of a dependend
        self.prj_to_mark = [x for x in Project._projects if x.is_project()]

        self.prj_done = []
        self.prj_skipped = []
        self.prj_err = []
        self.prj_dropped = []
        self.projects_to_do = list(projects)

        while self.projects_to_do:
            p = self.projects_to_do.pop(0)
            # save the vs environment
            saved_env = copy.copy(self.vs_env)
            try:
                st = time.time()
                if self.__build_one(p):
                    self.prj_skipped.append(p.name)
                else:
                    msg = '%-*s (%.3f s)' % (Project.name_len, p.name, time.time() - st, )
                    self.prj_done.append(msg)
            except KeyboardInterrupt:
                traceback.print_exc()
                log.error_exit("Interrupted on %s" % (p.name, ))
            except:
                traceback.print_exc()
                log.end(mark_error=True)
                if self.opts.keep:
                    self.prj_err.append(p.name)
                    self._drop_proj(p)
                else:
                    log.error_exit("%s build failed" % (p.name, ))
            self.vs_env = saved_env

        script_title(None)
        if self.prj_done:
            log.message('')
            log.message('Project(s) built:')
            for p in self.prj_done:
                log.message('    %s' % (p, ))

        if self.prj_skipped:
            log.message('')
            log.message('Project(s) skipped (already built):')
            for p in self.prj_skipped:
                log.message('    %s' % (p, ))

        if self.prj_err:
            log.message('')
            log.message('Project(s) not built:')
            for p in self.prj_err:
                log.message('    %s' % (p, ))

            miss = len(self.prj_err)
            if self.prj_dropped:
                log.message('')
                log.message('Missing dependecies:')
                for p in self.prj_dropped:
                    log.message('    %s' % (p, ))
                miss += len(self.prj_dropped)

            # Don't fool appveyor
            log.error_exit('%u project(s) missing ;(' % (miss, ))

        log.close()

    def __prepare_build(self, projects):
        if not os.path.exists(self.working_dir):
            log.log("Creating working directory %s" % (self.working_dir,))
            os.makedirs(self.working_dir)

        shutil.copy(os.path.join(self.opts.patches_root_dir, 'stack.props'), self.working_dir)

        build_dir = os.path.join(self.working_dir, '..', '..', '..', 'gtk', self.opts.platform)
        if not os.path.exists(build_dir):
            log.log("Creating directory %s" % (build_dir,))
            os.makedirs(build_dir)

        script_title('* Downloading')
        log.start('Downloading packages')
        for p in projects:
            if self.__download_one(p):
                return True
        log.end()

        return False

    def _load_built_files(self):
        """
        Return a set with all the files present in the final, installation, dir
        """
        return dirlist2set(self.gtk_dir)

    def __build_one(self, proj):
        """
        Build one project, return True if skipped
        """
        # Check if we update the tarball / git
        proj.builder = self
        self.__project = proj
        proj.prepare_build_dir()

        if self.opts.fast_build and not proj.clean:
            t = proj.mark_file_exist()
            if t:
                log.message("Fast build:skipping project %s, built @ %s" % (proj.name, t, ))
                proj.builder = None
                self.__project = None
                return True

        proj.mark_file_remove()
        log.start("Building project %s (%s)" % (proj.name, proj.version, ))
        script_title('%s (%s)' % (proj.name, proj.version, ))

        proj.pkg_dir = proj.build_dir + "-rel"
        shutil.rmtree(proj.pkg_dir, ignore_errors=True)
        os.makedirs(proj.pkg_dir)

        # Original path, converted to list
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
            # Extra enviroment from the dependency, normally the tools ...
            d.apply_extra_env(self.vs_env)

        # Make the (eventually) new path
        self.vs_env['PATH'] = ';'.join(paths)

        proj.patch()
        skip_deps = proj.build()

        log.debug("copying %s to %s" % (proj.pkg_dir, self.gtk_dir))
        self.copy_all(proj.pkg_dir, self.gtk_dir)
        shutil.rmtree(proj.pkg_dir, ignore_errors=True)

        proj.post_install()

        proj.builder = None
        self.__project = None

        if self.opts.make_zip:
            # Create file list
            cur = self._load_built_files()
            # delta with the old
            new = cur - self.file_built
            if new:
                # file presents, do the zip (with the version)
                if proj.version.startswith('git/'):
                    t_ver = proj.version[4:]
                else:
                    t_ver = proj.version

                _t = [ c if c.isalnum() else '_' for c in t_ver ]
                ver_part = ''.join(_t)

                zip_file = os.path.join(self.zip_dir, proj.prj_dir + '-' + ver_part)
                self.make_zip(zip_file, new)
                # use the current file set
                self.file_built = cur
            else:
                # No file preentt
                log.log("%s:zip not needed (tool?)" % (proj.name, ))

        # Drop the mark file for all the projects that depends on this so we rebuild them
        if not skip_deps:
            first = True
            for p in self.prj_to_mark:
                if proj in p.all_dependencies:
                    if first:
                        first = False
                        log.debug('Forcing build of %s dependent' % (proj.name, ))
                    log.debug(" > Mark %s ..." % (p.name, ))
                    p.mark_file_remove()
                    self.prj_to_mark.remove(p)

        # Mark this project done correctly
        proj.mark_file_write()

        script_title(None)
        log.end()
        return False

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
        #log.debug("__copy_to %s %s" % (src, destdir))
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
            log.debug("copying '%s' to '%s'" % (src, dst))
            shutil.copytree(src, dst)
        else:
            log.debug("copying '%s' to '%s'" % (src, destdir))
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
                log.message("Hash mismatch on %s:\n  Calculated '%s'\n  Expected   '%s'\n" % (proj.archive_file, hc, proj.hash, ))
                return True

            # Print the correct hash
            if self.opts.check_hash:
                log.message("Hash ok on %s (%s)" % (proj.archive_file, hc, ))
            else:
                log.debug("Hash ok on %s (%s)" % (proj.archive_file, hc, ))
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
            log.debug("archive file is not specified for project %s, skipping" % (proj.name,))
            return False

        if os.path.exists(proj.archive_file):
            log.debug("archive %s already exists" % (proj.archive_file,))
            return self.__check_hash(proj)

        if not os.path.exists(self.opts.archives_download_dir):
            log.log("Creating archives download directory %s" % (self.opts.archives_download_dir,))
            os.makedirs(self.opts.archives_download_dir)

        log.start_verbose("Downloading %s" % (proj.archive_file,))
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
        log.end()

        print('%-*s' % (self._old_print, '%s - Download finished' % (proj.archive_file, )), )
        return self.__check_hash(proj)

    def __sub_vars(self, s):
        if '%' in s:
            d = dict(platform=self.opts.platform, configuration=self.opts.configuration, build_dir=self.opts.build_dir, vs_ver=self.opts.vs_ver,
                     gtk_dir=self.gtk_dir,
                     vs_ver_year=self.vs_ver_year, )
            python = None
            if self.__project is not None:
                d['pkg_dir'] = self.__project.pkg_dir
                d['build_dir'] = self.__project.build_dir
                # Add python & perl only if the project depends on them
                p = Project.get_project('python')
                if p in self.__project.all_dependencies:
                    python = Project.get_tool_path(p)
                    d['python_dir'] = python

                p = Project.get_project('perl')
                if p in self.__project.all_dependencies:
                    perl = Project.get_tool_base_dir(p)
                    d['perl_dir'] = perl

            d['msbuild_opts'] = self._create_msbuild_opts(python)
            return s % d
        else:
            return s

    def exec_vs(self, cmd, working_dir=None, add_path=None):
        self.__execute(self.__sub_vars(cmd), working_dir=working_dir, add_path=add_path, env=self.vs_env)

    def exec_cargo(self, params='', working_dir=None, rustc_opts=None):
        cmd = 'cargo'
        if self.opts.cargo_opts:
            cmd += ' ' + self.opts.cargo_opts
        if params:
            cmd += ' ' + params

        cargo_home = Project.get_tool_path('cargo')

        env = os.environ.copy()
        env['RUSTUP_HOME'] = cargo_home
        env['CARGO_HOME'] = cargo_home           
        if rustc_opts is not None:
            env.update(rustc_opts)
            
        # set platform
        rustup = os.path.join(cargo_home, 'bin', 'rustup.exe')
        self.__execute('%s default stable-%s-pc-windows-msvc' % (rustup, 'i686' if self.x86 else 'x86_64'),
                       env=env)

        # build
        self.__execute(self.__sub_vars(cmd),
                       working_dir=working_dir,
                       add_path=os.path.join(cargo_home, 'bin'),
                       env=env)

    def exec_cmd(self, cmd, working_dir=None, add_path=None):
        self.__execute(self.__sub_vars(cmd), working_dir=working_dir, add_path=add_path)

    def exec_ninja(self, params='', working_dir=None, add_path=None):
        cmd = 'ninja'
        if self.opts.ninja_opts:
            cmd += ' ' + self.opts.ninja_opts
        if params:
            cmd += ' ' + params
        self.__execute(self.__sub_vars(cmd), working_dir=working_dir, add_path=add_path, env=self.vs_env)

    def install(self, build_dir, pkg_dir, *args):
        if len(args) == 1:
            args = args[0].split()
        dest = os.path.join(pkg_dir, self.__sub_vars(args[-1]))
        self.make_dir(dest)
        for f in args[:-1]:
            src = os.path.join(self.__sub_vars(build_dir), self.__sub_vars(f))
            log.debug("copying %s to %s" % (src, dest))
            self.__copy_to(src, dest)

    def install_dir(self, build_dir, pkg_dir, src, dest):
        src = os.path.join(build_dir, self.__sub_vars(src))
        dest = os.path.join(pkg_dir, self.__sub_vars(dest))
        log.debug("copying %s content to %s" % (src, dest))
        self.copy_all(src, dest)

    def exec_msys(self, args, working_dir=None):
        self.__execute(args, working_dir=working_dir, add_path=os.path.join(self.opts.msys_dir, 'usr', 'bin'))

    def __execute(self, args, working_dir=None, add_path=None, env=None):
        log.debug("running %s, cwd=%s, path+=%s" % (args, working_dir, add_path))
        if add_path:
            if env is not None:
                env = dict(env)
            else:
                env = dict(os.environ)
            self.__add_path(env, add_path)
        if self.opts.capture_out:
            try:
                res = subprocess.run(args, cwd=working_dir, env=env, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, errors='ignore')
            except subprocess.CalledProcessError as e:
                # Dump the lines that leads to the error
                log.messages_dump(e.stdout, "Error building '%s'" % (self.__project.name))
                # and let the caller handle this
                raise

            log.messages_dump(res.stdout, prt=self.opts.print_out)
        else:
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
        log.debug("Changed path env variable to '%s'" % env[key])
