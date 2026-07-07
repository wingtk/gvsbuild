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

"""Offline mirror support for git-based projects.

git projects are normally cloned from their upstream repository at build time.
To support fully offline builds (and to populate a source mirror), this module
can archive a whole checkout - including the .git directory - into a single zip
under the archives download dir, and later reconstruct it without any network
access.

The functions here take a GitRepo-like object exposing: name, tag, repository,
fetch_submodules, and opts (with archives_download_dir and git_expand_dir).
"""

import glob
import os
import subprocess
import zipfile
from datetime import datetime, timezone
from pathlib import Path

from .simple_ui import log
from .utils import rmtree_full

_ARCHIVE_SUFFIX = ".git.zip"


def _git_mirror_dir(repo):
    return os.path.join(repo.opts.archives_download_dir, "git")


def mirror_archive_write_path(repo, commit):
    """Path of the offline mirror archive for a git project, named by the
    resolved commit hash and download timestamp. The hash is a stable content
    identifier regardless of whether the project pins a full hash, a short hash
    or a branch/tag; the timestamp lets us prefer the newest cached snapshot
    when multiple archives exist."""
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
    return os.path.join(
        _git_mirror_dir(repo), f"{repo.name}-{commit}-{stamp}{_ARCHIVE_SUFFIX}"
    )


def _archive_name_parts(repo, path):
    """Return (commit, timestamp) for a mirror archive path, or None."""
    filename = os.path.basename(path)
    prefix = f"{repo.name}-"
    if not filename.startswith(prefix) or not filename.endswith(_ARCHIVE_SUFFIX):
        return None

    body = filename[len(prefix) : -len(_ARCHIVE_SUFFIX)]
    try:
        commit, stamp = body.rsplit("-", 1)
    except ValueError:
        return None

    return commit, stamp


def _find_mirror_archive_for_commit(repo, commit):
    """Locate the cached archive for a specific commit hash, if present."""
    matches = glob.glob(
        os.path.join(_git_mirror_dir(repo), f"{repo.name}-{commit}-*{_ARCHIVE_SUFFIX}")
    )
    if not matches:
        return None

    return max(matches, key=lambda path: _archive_name_parts(repo, path)[1])


def find_mirror_archive(repo):
    """Locate the offline mirror archive for a git project without any network
    access. The commit hash in the name cannot be recomputed offline, so match
    by project name and prefer the most recently downloaded snapshot. Returns
    the path or None if not present."""
    matches = []
    for path in glob.glob(
        os.path.join(_git_mirror_dir(repo), f"{repo.name}-*{_ARCHIVE_SUFFIX}")
    ):
        parts = _archive_name_parts(repo, path)
        if parts:
            matches.append((parts[1], path))

    if not matches:
        return None

    return max(matches, key=lambda item: item[0])[1]


def _walk_files(root):
    """Return every file/dir path under root, preserving case (unlike
    dirlist2set, which lowercases names for the Windows build)."""
    paths = []
    for dirpath, dirnames, filenames in os.walk(root):
        for name in dirnames:
            paths.append(os.path.join(dirpath, name))
        for name in filenames:
            paths.append(os.path.join(dirpath, name))
    return paths


def _resolve_commit(dest):
    """Return the full commit hash checked out at dest."""
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=dest, text=True
    ).strip()


def create_mirror_archive(repo, src_dir):
    """Zip the whole checkout at src_dir (including .git) into the offline
    mirror archive, named by the resolved commit hash."""
    commit = _resolve_commit(src_dir)
    mirror = _find_mirror_archive_for_commit(repo, commit)
    if mirror:
        log.debug(f"(git) mirror archive for {repo.name} at {commit} already exists")
        return

    mirror = mirror_archive_write_path(repo, commit)
    os.makedirs(os.path.dirname(mirror), exist_ok=True)
    log.start(f"(git) Creating mirror archive {mirror}")
    files = _walk_files(src_dir)
    with zipfile.ZipFile(mirror, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for f in sorted(files):
            zf.write(f, arcname=os.path.relpath(f, src_dir))
    log.end()


def restore_mirror_archive(repo, dest):
    """Reconstruct the checkout at dest from the offline mirror archive.
    Returns True on success, False if the archive is missing."""
    mirror = find_mirror_archive(repo)
    if not mirror:
        return False
    log.start(f"(git) Restoring {dest} from mirror archive {mirror}")
    os.makedirs(dest, exist_ok=True)
    dest_path = Path(dest).resolve()
    with zipfile.ZipFile(mirror, "r") as zf:
        for member in zf.namelist():
            member_path = (dest_path / member).resolve()
            if not member_path.is_relative_to(dest_path):
                raise RuntimeError(f"Unsafe path in mirror archive: {member}")
            zf.extract(member, dest)
    log.end()
    return True


def fetch_to_mirror(repo):
    """Clone the repository and create the offline mirror archive, using plain
    git (not msys) so it can run on any platform. The archive path is keyed by
    the resolved commit hash, so a changed checkout gets a new archive."""
    dest = os.path.join(repo.opts.git_expand_dir, repo.name)
    os.makedirs(repo.opts.git_expand_dir, exist_ok=True)
    if os.path.isdir(dest):
        rmtree_full(dest)

    log.start(f"(git) Cloning {repo.repository} to {dest}")
    subprocess.check_call(["git", "clone", repo.repository, dest])
    if repo.tag:
        subprocess.check_call(["git", "checkout", "-f", repo.tag], cwd=dest)
    if repo.fetch_submodules:
        subprocess.check_call(["git", "submodule", "update", "--init"], cwd=dest)
    log.end()

    create_mirror_archive(repo, dest)
