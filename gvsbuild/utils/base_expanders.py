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
Various downloader / unpacker (tar, git, hg, ...)
"""

import os
import shutil
import zipfile
import tarfile
import hashlib

from .simple_ui import log
from .utils import rmtree_full

def read_mark_file(directory, file_name='.wingtk-extracted-file'):
    """"
    Read a single line from file, returning an empty string on error
    """
    rt = ''
    try:
        with open(os.path.join(directory, file_name), 'rt') as fi:
            rt = fi.readline().strip()
    except IOError as e:
        log.debug("Exception on reading from '%s'" % (file_name, ))
        log.debug("%s" % (e, ))

    return rt

def write_mark_file(directory, val, file_name='.wingtk-extracted-file'):
    """
    Write the value (filename or content hash) to the mark file
    """
    with open(os.path.join(directory, file_name), 'wt') as fo:
        fo.write('%s\n' % (val, ))

def extract_exec(src, dest_dir, dir_part=None, strip_one=False, check_file=None, force_dest=None, check_mark=False):
    """
    Extract (or copy, in case of an exe file) from src to dest_dir,
    handling the strip of the first part of the path in case of the tarbombs.

    dir_part is a piece, present in the tar/zip file, added to the desst_dir for
    the checks

    if check_file is passed and is present in the filesystem the extract is
    skipped (tool alreay installed)

    force_dest can be used only on the exe file and set the destination name

    with check_mark the name of the original file extracted is written in the
    destination dir and checked, forcing a new, clean, extraction
    
    Returns True if the extraction has been done, False if it's skipped (so we can skip 
    marking the dependents of the project/tool)
    """

    # Support function
    def __get_stripped_tar_members(tar):
        for tarinfo in tar.getmembers():
            path = tarinfo.name.split('/')
            if len(path) == 1:
                if tarinfo.isdir():
                    continue
                else:
                    raise Exception('Cannot strip directory prefix from tar with top level files')
            tarinfo.name = '/'.join(path[1:])
            if tarinfo.issym() or tarinfo.islnk():
                tarinfo.linkname = '/'.join(tarinfo.linkname.split('/')[1:])
            yield tarinfo

    if dir_part:
        full_dest = os.path.join(dest_dir, dir_part)
    else:
        full_dest = dest_dir

    if check_mark:
        rd_file = read_mark_file(full_dest)
        wr_file = os.path.basename(src)
        if rd_file != wr_file:
            log.log('Forcing extraction of %s' % (src, ))
            rmtree_full(full_dest, retry=True)
            check_file = None
        else:
            # ok, finish, we've done
            return False

    if check_file is not None:
        if check_file:
            # look for the specific file
            if os.path.isfile(check_file):
                log.debug('Skipping %s handling, %s present' % (src, check_file, ))
                return False
        else:
            # If the directory exist we are ok
            if os.path.exists(full_dest):
                log.debug('Skipping %s handling, directory exists' % (src, ))
                return False

    log.log('Extracting %s to %s' % (src, full_dest, ))
    os.makedirs(full_dest, exist_ok=True)

    _n, ext = os.path.splitext(src.lower())
    if ext == '.exe':
        # Exe file, copy directly
        if force_dest:
            shutil.copy2(src, force_dest)
        else:
            shutil.copy2(src, dest_dir)
    elif ext == '.zip':
        # Zip file
        with zipfile.ZipFile(src) as zf:
            if strip_one:
                members = zf.infolist()
                for m in members:
                    if m.is_dir():
                        continue
                    cl = m.filename.split('/')
                    if len(cl) > 1:
                        m.filename = '/'.join(cl[1:])
                        
                    zf.extract(m, path=dest_dir)
            else:
                zf.extractall(path=dest_dir)
    else:
        # Ok, hoping it's a tarfile we can handle :)
        with tarfile.open(src) as tar:
            tar.extractall(dest_dir, __get_stripped_tar_members(tar) if strip_one else tar.getmembers())

    if check_mark:
        # write the data
        write_mark_file(full_dest, wr_file)

    # Say that we have done the extraction
    return True

def dirlist2set(st_dir, add_dirs=False, skipped_dir=None):
    """
    Loads & return a set with all the files and, eventually,
    directory from a single dir.

    Used to make a file list to create a .zip file
    """
    def _load_single_dir(dir_name, returned_set, skipped_dir):
        for cf in os.scandir(dir_name):
            full = os.path.join(dir_name, cf.name.lower())
            if cf.is_file():
                returned_set.add(full)
            elif cf.is_dir():
                if cf.name.lower() in skipped_dir:
                    log.debug("  Skipped dir '%s' (from '%s')" % (cf.name, dir_name, ))
                else:
                    if (add_dirs):
                        returned_set.add(full)
                    _load_single_dir(full, returned_set, skipped_dir)
    rt = set()
    if skipped_dir is None:
        skipped_dir = []
    skipped_dir.append('__pycache__')
    try:
        log.debug("Getting file list from '%s'" % (st_dir, ))
        _load_single_dir(st_dir, rt, set(skipped_dir))
    except FileNotFoundError:
        print("Warning: (--zip-continue) No file found on '%s'" % (st_dir, ))
    return rt

def make_zip_hash(files):
    """"
    Calculate an hash of all the files to put in a zip file
    """
    hash_calc = hashlib.sha256()
    for file_name in sorted(list(files)):
        # add also the file full path, to support only moving files in the zip
        hash_calc.update(file_name.lower().encode('utf-8'))
        if os.path.isfile(file_name):
            # add the file content
            with open(file_name, 'rb') as fi:
                for chunk in iter(lambda: fi.read(4096), b""):
                    hash_calc.update(chunk)

    return hash_calc.hexdigest()

def make_zip(name, files, skip_spc=0):
    """
    Create the name .zip using all files. skip_spc spaces are dropped
    from the beginning of all file/dir names to avoid to have the full
    path (e.g. from c:\data\temp\build\my_arch we want to save only
    mt_arch
    """
    log.start_verbose('Creating zip file %s with %u files' % (name, len(files), ))
    with zipfile.ZipFile(name + '.zip', 'w', compression=zipfile.ZIP_DEFLATED) as zf:
        for f in sorted(list(files)):
            zf.write(f, arcname=f[skip_spc:])
    log.end()

class Tarball(object):
    def update_build_dir(self):
        log.start_verbose('(tar) Updating %s' % (self.archive_file, ))
        rt = extract_exec(self.archive_file, self.build_dir, strip_one=not self.tarbomb, check_mark=True)
        log.end()
        return rt

    def unpack(self):
        log.start_verbose('(tar) Extracting %s' % (self.archive_file, ))
        extract_exec(self.archive_file, self.build_dir, strip_one=not self.tarbomb, check_mark=True)
        log.end()

class MercurialRepo(object):
    def unpack(self):
        log.start_verbose('(hg) Cloning %s to %s' % (self.repo_url, self.build_dir))
        self.exec_cmd('hg clone %s %s-tmp' % (self.repo_url, self.build_dir))
        shutil.move(self.build_dir + '-tmp', self.build_dir)
        log.end()

    def update_build_dir(self):
        log.start_verbose('(hg) Updating directory %s' % (self.build_dir,))
        self.exec_cmd('hg pull -u', working_dir=self.build_dir)
        log.end()

class GitRepo(object):
    def read_temp_hash(self):
        return read_mark_file(self.opts.git_expand_dir, self.name + '.hash')
    
    def write_temp_hash(self, hash_val):
        write_mark_file(self.opts.git_expand_dir, hash_val, self.name + '.hash')

    def get_tag_name(self, src_dir):
        if self.tag:
            # name the .zip from the tag, validating it
            t_name = [ c if c.isalnum() else '_' for c in self.tag ]
            tag_name = ''.join(t_name)
        else:
            of = os.path.join(src_dir, '.git-temp.rsp')
            self.builder.exec_msys('git rev-parse --short HEAD >%s' % (of, ), working_dir=src_dir)
            with open(of, 'rt') as fi:
                tag_name = fi.readline().rstrip('\n')
            os.remove(of)

        return tag_name

    def create_zip(self):
        """
        Create a .zip file with the git checkout to be able to
        work offline and as a reference of the last correct build
        """
        src_dir = os.path.join(self.opts.git_expand_dir, self.name)
        zip_post = self.get_tag_name(src_dir)

        # Be sure to have the git .zip dir
        git_tmp_dir = os.path.join(self.builder.opts.archives_download_dir, 'git')
        if not os.path.exists(git_tmp_dir):
            log.log("Creating git archives save directory %s" % (git_tmp_dir, ))
            os.makedirs(git_tmp_dir)

        # check if some file has changed
        all_files = dirlist2set(src_dir, add_dirs=True, skipped_dir=[ '.git', ])
        n_hash = make_zip_hash(all_files)
        o_hash = self.read_temp_hash() if not self.clean else None
        upd_build_dir = False
        if o_hash != n_hash:
            # create a .zip file with the downloaded project
            make_zip(os.path.join(git_tmp_dir, self.prj_dir + '-' + zip_post), all_files, len(src_dir))
            # update the hash 
            self.write_temp_hash(n_hash)
            # copy the git buffer to the working dir, cleaning up before copying
            upd_build_dir = True
            if os.path.isdir(self.build_dir):
                rmtree_full(self.build_dir)

        if not upd_build_dir:
            # Check if the destination dir exists
            if not os.path.isdir(self.build_dir):
                upd_build_dir = True
            else:
                o_hash = read_mark_file(self.build_dir)
                if o_hash != n_hash:
                    upd_build_dir = True
                    rmtree_full(self.build_dir)

        if upd_build_dir:
            shutil.copytree(src_dir, self.build_dir)
            write_mark_file(self.build_dir, n_hash)

        return upd_build_dir

    def unpack(self):
        self.update_build_dir()

    def _update_dir(self, remove_dest=False):

        dest = os.path.join(self.opts.git_expand_dir, self.name)
        if self.clean or remove_dest:
            if os.path.isdir(dest):
                rmtree_full(dest)

        if os.path.isdir(dest):
            # Update 
            log.start('(git) Updating directory %s' % (dest, ))

            if self.tag:
                self.builder.exec_msys('git fetch origin', working_dir=dest)
                self.builder.exec_msys('git checkout -f %s' % self.tag, working_dir=dest)
            else:
                self.builder.exec_msys('git checkout -f', working_dir=dest)
                self.builder.exec_msys('git pull --rebase', working_dir=dest)

            if self.fetch_submodules:
                log.start_verbose('Update submodule(s)')
                self.builder.exec_msys('git submodule update --init', working_dir=dest)
                log.end()
            rt = self.create_zip()
        else:
            log.start('(git) Cloning %s to %s' % (self.repo_url, dest))

            self.builder.exec_msys('git clone %s %s' % (self.repo_url, dest))

            if self.tag:
                self.builder.exec_msys('git checkout -f %s' % self.tag, working_dir=dest)
    
            if self.fetch_submodules:
                log.start_verbose('Fetch submodule(s)')
                self.builder.exec_msys('git submodule update --init',  working_dir=dest)
                log.end()
            self.create_zip()
            rt = True
        
        return rt

    def update_build_dir(self):
        rt = None
        if not os.path.exists(self.opts.git_expand_dir):
            log.log("Creating git expoand directory %s" % (self.opts.git_expand_dir,))
            os.makedirs(self.opts.git_expand_dir, exist_ok=True)

        try:
            rt = self._update_dir()
        except Exception as e:
            log.message('%s:Exception %s' % (self.name, e, ))
            log.message('Removing the destination dir ...')
            rt = self._update_dir(remove_dest=True)

        if rt:
            if os.path.exists(self.patch_dir):
                log.log("Copying files from %s to %s" % (self.patch_dir, self.build_dir))
                self.builder.copy_all(self.patch_dir, self.build_dir)
        log.end()
        return rt

class NullExpander(object):
    """
    Null expander to use when all the source are present in the script and
    nothing must be downloaded

    """
    def update_build_dir(self):
        # Force the copy of the files in the script
        return True

    def unpack(self):
        # Everything is in our script, nothing to download
        pass

