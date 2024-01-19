#  Copyright (C) 2016 The Gvsbuild Authors
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

"""Various downloader / unpacker (tar, git, ...)"""

import hashlib
import os
import shutil
import tarfile
import zipfile

from .simple_ui import log
from .utils import rmtree_full


def read_mark_file(directory, file_name=".wingtk-extracted-file"):
    """Read a single line from file, returning an empty string on error."""
    rt = ""
    try:
        with open(os.path.join(directory, file_name), encoding="utf-8") as fi:
            rt = fi.readline().strip()
    except OSError as e:
        log.debug(f"Exception on reading from '{file_name}'")
        log.debug(f"{e}")

    return rt


def write_mark_file(directory, val, file_name=".wingtk-extracted-file"):
    """Write the value (filename or content hash) to the mark file."""
    with open(os.path.join(directory, file_name), "w", encoding="utf-8") as fo:
        fo.write(f"{val}\n")


def extract_exec(
    src,
    dest_dir,
    dir_part=None,
    strip_one=False,
    check_file=None,
    force_dest=None,
    check_mark=False,
):
    """Extract (or copy, in case of an exe file) from src to dest_dir, handling
    the strip of the first part of the path in case of the tarbombs.

    dir_part is a piece, present in the tar/zip file, added to the dest_dir for
    the checks

    if check_file is passed and is present in the filesystem the extract is
    skipped (tool already installed)

    force_dest can be used only on the exe file and set the destination name

    with check_mark the name of the original file extracted is written in the
    destination dir and checked, forcing a new, clean, extraction

    Returns True if the extraction has been done, False if it's skipped (so we can skip
    marking the dependents of the project/tool)
    """

    # Support function
    def __get_stripped_tar_members(tar):
        for tarinfo in tar.getmembers():
            path = tarinfo.name.split("/")
            if len(path) == 1:
                if tarinfo.isdir():
                    continue
                else:
                    raise NotADirectoryError(
                        "Cannot strip directory prefix from tar with top level files"
                    )
            tarinfo.name = "/".join(path[1:])
            if tarinfo.issym() or tarinfo.islnk():
                tarinfo.linkname = "/".join(tarinfo.linkname.split("/")[1:])
            yield tarinfo

    full_dest = os.path.join(dest_dir, dir_part) if dir_part else dest_dir
    if check_mark:
        rd_file = read_mark_file(full_dest)
        wr_file = os.path.basename(src)
        if rd_file != wr_file:
            log.log(f"Forcing extraction of {src}")
            rmtree_full(full_dest, retry=True)
            check_file = None
        else:
            # ok, finish, we've done
            return False

    if check_file is not None:
        if check_file:
            # look for the specific file
            if os.path.isfile(check_file):
                log.debug(f"Skipping {src} handling, {check_file} present")
                return False
        else:
            # If the directory exist we are ok
            if os.path.exists(full_dest):
                log.debug(f"Skipping {src} handling, directory exists")
                return False

    log.log(f"Extracting {src} to {full_dest}")
    os.makedirs(full_dest, exist_ok=True)

    _n, ext = os.path.splitext(src.lower())
    if ext == ".exe":
        # Exe file, copy directly
        if force_dest:
            shutil.copy2(src, force_dest)
        else:
            shutil.copy2(src, dest_dir)
    elif ext == ".zip":
        # Zip file
        with zipfile.ZipFile(src) as zf:
            if strip_one:
                members = zf.infolist()
                for m in members:
                    if m.is_dir():
                        continue
                    cl = m.filename.split("/")
                    if len(cl) > 1:
                        m.filename = "/".join(cl[1:])

                    zf.extract(m, path=dest_dir)
            else:
                zf.extractall(path=dest_dir)
    else:
        # Ok, hoping it's a tarfile we can handle :)
        with tarfile.open(src) as tar:
            tar.extractall(
                dest_dir,
                __get_stripped_tar_members(tar) if strip_one else tar.getmembers(),
            )

    if check_mark:
        # write the data
        write_mark_file(full_dest, wr_file)

    # Say that we have done the extraction
    return True


def dirlist2set(st_dir, add_dirs=False, skipped_dir=None):
    """Loads & return a set with all the files and, eventually, directory from
    a single dir.

    Used to make a file list to create a .zip file
    """

    def _load_single_dir(dir_name, returned_set, skipped_dir):
        for cf in os.scandir(dir_name):
            full = os.path.join(dir_name, cf.name.lower())
            if cf.is_file():
                returned_set.add(full)
            elif cf.is_dir():
                if cf.name.lower() in skipped_dir:
                    log.debug(f"  Skipped dir '{cf.name}' (from '{dir_name}')")
                else:
                    if add_dirs:
                        returned_set.add(full)
                    _load_single_dir(full, returned_set, skipped_dir)

    rt = set()
    if skipped_dir is None:
        skipped_dir = []
    skipped_dir.append("__pycache__")
    try:
        log.debug(f"Getting file list from '{st_dir}'")
        _load_single_dir(st_dir, rt, set(skipped_dir))
    except FileNotFoundError:
        print(f"Warning: (--zip-continue) No file found on '{st_dir}'")
    return rt


def make_zip_hash(files):
    """Calculate an hash of all the files to put in a zip file."""
    hash_calc = hashlib.sha256()
    for file_name in sorted(files):
        # add also the file full path, to support only moving files in the zip
        hash_calc.update(file_name.lower().encode("utf-8"))
        if os.path.isfile(file_name):
            # add the file content
            with open(file_name, "rb") as fi:
                for chunk in iter(lambda: fi.read(4096), b""):
                    hash_calc.update(chunk)

    return hash_calc.hexdigest()


def make_zip(name, files, skip_spc=0):
    """Create the name .zip using all files.

    skip_spc spaces are dropped from the beginning of all file/dir names
    to avoid to have the full path (e.g. from
    c:\\data\temp\build\\my_arch we want to save only mt_arch
    """
    log.start_verbose(f"Creating zip file {name} with {len(files)} files")
    with zipfile.ZipFile(f"{name}.zip", "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for f in sorted(files):
            zf.write(f, arcname=f[skip_spc:])
    log.end()


class Tarball:
    def update_build_dir(self):
        log.start_verbose(f"(tar) Updating {self.archive_file}")
        rt = extract_exec(
            self.archive_file,
            self.build_dir,
            strip_one=not self.tarbomb,
            check_mark=True,
        )
        log.end()
        return rt

    def unpack(self):
        log.start_verbose(f"(tar) Extracting {self.archive_file}")
        extract_exec(
            self.archive_file,
            self.build_dir,
            strip_one=not self.tarbomb,
            check_mark=True,
        )
        log.end()

    def export(self):
        log.start(f"(tar) Exporting {self.name}")

        path = os.path.join(self.export_dir, f"{self.name}.zip")
        with zipfile.ZipFile(path, "w") as zipped_path:
            log.log(f"(tar) Exporting {self.archive_file}")
            zipped_path.write(
                self.archive_file, arcname=os.path.basename(self.archive_file)
            )

            for p in self.patches:
                log.log(f"(tar) Exporting {p}")
                zipped_path.write(
                    os.path.join(self.build_dir, p),
                    arcname=f"patches/{os.path.basename(p)}",
                )

        log.end()


class GitRepo:
    def read_temp_hash(self):
        return read_mark_file(self.opts.git_expand_dir, f"{self.name}.hash")

    def write_temp_hash(self, hash_val):
        write_mark_file(self.opts.git_expand_dir, hash_val, f"{self.name}.hash")

    def get_tag_name(self, src_dir):
        if self.tag:
            # name the .zip from the tag, validating it
            t_name = [c if c.isalnum() else "_" for c in self.tag]
            tag_name = "".join(t_name)
        else:
            of = os.path.join(src_dir, ".git-temp.rsp")
            self.builder.exec_msys(
                f"git rev-parse --short HEAD >{of}", working_dir=src_dir
            )
            with open(of, encoding="utf-8") as fi:
                tag_name = fi.readline().rstrip("\n")
            os.remove(of)

        return tag_name

    def create_zip(self):
        """Create a .zip file with the git checkout to be able to work offline
        and as a reference of the last correct build."""
        src_dir = os.path.join(self.opts.git_expand_dir, self.name)
        zip_post = self.get_tag_name(src_dir)

        # Be sure to have the git .zip dir
        git_tmp_dir = os.path.join(self.builder.opts.archives_download_dir, "git")
        if not os.path.exists(git_tmp_dir):
            log.log(f"Creating git archives save directory {git_tmp_dir}")
            os.makedirs(git_tmp_dir)

        # check if some file has changed
        all_files = dirlist2set(
            src_dir,
            add_dirs=True,
            skipped_dir=[
                ".git",
            ],
        )
        n_hash = make_zip_hash(all_files)
        o_hash = None if self.clean else self.read_temp_hash()
        upd_build_dir = False
        if o_hash != n_hash:
            # create a .zip file with the downloaded project
            make_zip(
                os.path.join(git_tmp_dir, f"{self.prj_dir}-{zip_post}"),
                all_files,
                len(src_dir),
            )

            # update the hash
            self.write_temp_hash(n_hash)
            # copy the git buffer to the working dir, cleaning up before copying
            upd_build_dir = True
            if os.path.isdir(self.build_dir):
                rmtree_full(self.build_dir)

        if not upd_build_dir:
            if os.path.isdir(self.build_dir):
                o_hash = read_mark_file(self.build_dir)
                if o_hash != n_hash:
                    upd_build_dir = True
                    rmtree_full(self.build_dir)

            else:
                upd_build_dir = True
        if upd_build_dir:
            shutil.copytree(src_dir, self.build_dir)
            write_mark_file(self.build_dir, n_hash)

        return upd_build_dir

    def unpack(self):
        self.update_build_dir()

    def _update_dir(self, remove_dest=False):
        dest = os.path.join(self.opts.git_expand_dir, self.name)
        if (self.clean or remove_dest) and os.path.isdir(dest):
            rmtree_full(dest)

        if not os.path.isdir(dest):
            return self._clone_and_checkout(dest)
        # Update
        log.start(f"(git) Updating directory {dest}")

        if self.tag:
            self.builder.exec_msys("git fetch origin", working_dir=dest)
            self.builder.exec_msys(f"git checkout -f {self.tag}", working_dir=dest)
        else:
            self.builder.exec_msys("git checkout -f", working_dir=dest)
            self.builder.exec_msys("git pull --rebase", working_dir=dest)

        if self.fetch_submodules:
            self._update_submodules("Update submodule(s)", dest)
        return self.create_zip()

    def _clone_and_checkout(self, dest):
        log.start(f"(git) Cloning {self.repo_url} to {dest}")

        self.builder.exec_msys(f"git clone {self.repo_url} {dest}")

        if self.tag:
            self.builder.exec_msys(f"git checkout -f {self.tag}", working_dir=dest)

        if self.fetch_submodules:
            self._update_submodules("Fetch submodule(s)", dest)
        self.create_zip()
        return True

    def _update_submodules(self, log_value, dest):
        log.start_verbose(log_value)
        self.builder.exec_msys("git submodule update --init", working_dir=dest)
        log.end()

    def update_build_dir(self):
        rt = None
        if not os.path.exists(self.opts.git_expand_dir):
            log.log(f"Creating git expand directory {self.opts.git_expand_dir}")
            os.makedirs(self.opts.git_expand_dir, exist_ok=True)

        try:
            rt = self._update_dir()
        except Exception as e:
            log.message(f"{self.name}:Exception {e}")
            log.message("Removing the destination dir ...")
            rt = self._update_dir(remove_dest=True)

        if rt and os.path.exists(self.patch_dir):
            log.log(f"Copying files from {self.patch_dir} to {self.build_dir}")
            self.builder.copy_all(self.patch_dir, self.build_dir)
        log.end()
        return rt

    def export(self):
        log.start(f"(git) Exporting directory {self.build_dir}")

        src_dir = os.path.join(self.opts.git_expand_dir, self.name)
        filename = f"{self.name}-{self.get_tag_name(src_dir)}.zip"
        self.builder.exec_msys(
            f"git archive -o {filename} HEAD", working_dir=self.build_dir
        )

        path = os.path.join(self.export_dir, f"{self.name}.zip")
        with zipfile.ZipFile(path, "w") as zipped_path:
            log.log(f"(git) Exporting {filename}")
            zipped_path.write(os.path.join(self.build_dir, filename), arcname=filename)

            for p in self.patches:
                log.log(f"(git) Exporting {p}")
                zipped_path.write(
                    os.path.join(self.build_dir, p),
                    arcname=f"patches/{os.path.basename(p)}",
                )

        log.end()


class NullExpander:
    """Null expander to use when all the source are present in the script and
    nothing must be downloaded."""

    def update_build_dir(self):
        # Force the copy of the files in the script
        return True

    def unpack(self):
        # Everything is in our script, nothing to download
        pass

    def export(self):
        pass
