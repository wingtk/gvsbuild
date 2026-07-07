#  Copyright (C) 2026 The Gvsbuild Authors
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

import zipfile
from types import SimpleNamespace

from gvsbuild.utils import offline_repos


def _make_repo(tmp_path):
    return SimpleNamespace(
        name="foo",
        repository="https://example.invalid/foo.git",
        tag=None,
        fetch_submodules=False,
        opts=SimpleNamespace(
            archives_download_dir=str(tmp_path / "archives"),
            git_expand_dir=str(tmp_path / "git"),
        ),
    )


def test_find_mirror_archive_prefers_latest_timestamp(tmp_path):
    repo = _make_repo(tmp_path)
    mirror_dir = tmp_path / "archives" / "git"
    mirror_dir.mkdir(parents=True)

    older = mirror_dir / "foo-aaa-20260101T010101.000001Z.git.zip"
    newer = mirror_dir / "foo-bbb-20260102T010101.000001Z.git.zip"
    older.write_bytes(b"old")
    newer.write_bytes(b"new")

    assert offline_repos.find_mirror_archive(repo) == str(newer)


def test_create_mirror_archive_skips_existing_commit_snapshot(tmp_path, monkeypatch):
    repo = _make_repo(tmp_path)
    mirror_dir = tmp_path / "archives" / "git"
    mirror_dir.mkdir(parents=True)
    existing = mirror_dir / "foo-aaa-20260101T010101.000001Z.git.zip"
    existing.write_bytes(b"cached")

    monkeypatch.setattr(offline_repos, "_resolve_commit", lambda src_dir: "aaa")

    called = []

    def fail_if_called(*args, **kwargs):
        called.append(True)
        raise AssertionError("ZipFile should not be called for cached commits")

    monkeypatch.setattr(offline_repos.zipfile, "ZipFile", fail_if_called)
    monkeypatch.setattr(offline_repos.log, "debug", lambda *args, **kwargs: None)

    offline_repos.create_mirror_archive(repo, str(tmp_path))

    assert not called


def test_restore_mirror_archive_rejects_path_traversal(tmp_path, monkeypatch):
    repo = _make_repo(tmp_path)
    mirror_dir = tmp_path / "archives" / "git"
    mirror_dir.mkdir(parents=True)
    mirror = mirror_dir / "foo-aaa-20260101T010101.000001Z.git.zip"

    with zipfile.ZipFile(mirror, "w") as zf:
        zf.writestr("../outside.txt", "evil")

    monkeypatch.setattr(offline_repos, "find_mirror_archive", lambda _repo: str(mirror))
    monkeypatch.setattr(offline_repos.log, "start", lambda *args, **kwargs: None)
    monkeypatch.setattr(offline_repos.log, "end", lambda *args, **kwargs: None)

    dest = tmp_path / "restore"

    try:
        offline_repos.restore_mirror_archive(repo, str(dest))
    except RuntimeError as exc:
        assert "Unsafe path" in str(exc)
    else:
        raise AssertionError("restore_mirror_archive should reject traversal paths")
