#  Copyright (C) 2025 The Gvsbuild Authors
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
from __future__ import annotations

import sys
import tarfile
import zipfile
from collections.abc import Iterator
from contextlib import contextmanager
from io import BytesIO
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import Mock, patch

import pytest

from gvsbuild.utils.base_expanders import (
    _get_stripped_tar_members,
    _is_safe_link_target,
    _is_unsafe_path,
    _is_within_directory,
    _safe_extractall,
    _strip_path,
    extract_exec,
)


@contextmanager
def create_test_tar(
    files: dict[str, bytes | None], symlinks: dict[str, str] | None = None
) -> Iterator[tarfile.TarFile]:
    """
    Create a test tar file with specified files and symlinks.
    """
    tar_buffer = BytesIO()
    with tarfile.open(fileobj=tar_buffer, mode="w:gz") as tar:
        if files or symlinks:
            # Create base directory only if we have content
            base_info = tarfile.TarInfo("testdir")
            base_info.type = tarfile.DIRTYPE
            tar.addfile(base_info)

        # Add files
        for path, content in files.items():
            path = Path(path).as_posix()
            info = tarfile.TarInfo(f"testdir/{path}")
            if content is None:
                info.type = tarfile.DIRTYPE
            else:
                info.type = tarfile.REGTYPE
                info.size = len(content)
                content_buffer = BytesIO(content)
                tar.addfile(info, content_buffer)

        # Add symlinks
        if symlinks:
            for link_path, target in symlinks.items():
                link_path = Path(link_path).as_posix()
                target = Path(target).as_posix()
                info = tarfile.TarInfo(f"testdir/{link_path}")
                info.type = tarfile.SYMTYPE
                info.linkname = target
                tar.addfile(info)

    tar_buffer.seek(0)
    yield tarfile.open(fileobj=tar_buffer, mode="r:gz")


@pytest.fixture
def temp_workspace():
    """Create a temporary workspace with test files."""
    with TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Create test exe
        exe_path = temp_path / "test.exe"
        exe_path.write_bytes(b"fake exe content")

        # Create test zip with base directory
        zip_path = temp_path / "test.zip"
        with zipfile.ZipFile(zip_path, "w") as zf:
            zf.writestr("basedir/file1.txt", "content1")
            zf.writestr("basedir/subdir/file2.txt", "content2")

        # Create test tar with base directory
        tar_path = temp_path / "test.tar.gz"
        with tarfile.open(tar_path, "w:gz") as tar:
            base_info = tarfile.TarInfo("basedir")
            base_info.type = tarfile.DIRTYPE
            tar.addfile(base_info)

            info1 = tarfile.TarInfo("basedir/file1.txt")
            info1.size = 8
            tar.addfile(info1, BytesIO(b"content1"))

            info2 = tarfile.TarInfo("basedir/subdir/file2.txt")
            info2.size = 8
            tar.addfile(info2, BytesIO(b"content2"))

        yield temp_path


# Unit Tests: Path Manipulation
def test_strip_path():
    """Test the path stripping functionality."""
    assert _strip_path("testdir/file.txt") == "file.txt"


def test_strip_path_with_nested_directory():
    """Test stripping path with nested directories."""
    assert _strip_path("testdir/subdir/file.txt") == "subdir/file.txt"


def test_strip_path_without_directory():
    """Test stripping path without directory prefix."""
    assert _strip_path("file.txt") is None


def test_strip_path_base_directory():
    """Test stripping the base directory itself."""
    assert _strip_path("testdir") is None


# Unit Tests: Path Safety
def test_safe_paths():
    """Test identification of safe paths."""
    assert not _is_unsafe_path("file.txt")
    assert not _is_unsafe_path("dir/file.txt")
    assert not _is_unsafe_path("dir/subdir/file.txt")


def test_unsafe_windows_absolute_path():
    """Test identification of unsafe Windows absolute paths."""
    assert _is_unsafe_path("C:/file.txt")
    assert _is_unsafe_path("D:\\file.txt")


def test_unsafe_directory_traversal():
    """Test identification of unsafe directory traversal."""
    assert _is_unsafe_path("../file.txt")
    assert _is_unsafe_path("dir/../file.txt")
    assert _is_unsafe_path("dir/../../file.txt")


# Unit Tests: Directory Containment
def test_is_within_directory_valid_path():
    base = Path("/test/base")
    assert _is_within_directory(base / "file.txt", base) is True


def test_is_within_directory_valid_subdir():
    base = Path("/test/base")
    assert _is_within_directory(base / "subdir" / "file.txt", base) is True


def test_is_within_directory_parent_traversal():
    base = Path("/test/base")
    assert _is_within_directory(base / ".." / "file.txt", base) is False


def test_is_within_directory_deep_traversal():
    base = Path("/test/base")
    assert (
        _is_within_directory(base / "subdir" / ".." / ".." / "file.txt", base) is False
    )


def test_is_within_directory_absolute_path():
    base = Path("/test/base")
    assert _is_within_directory(Path("/other/path/file.txt"), base) is False


def test_is_within_directory_same_directory():
    base = Path("/test/base")
    assert _is_within_directory(base, base) is True


# Unit Tests: Link Safety
def test_safe_link_target_to_existing_file():
    """Test link targeting an existing file."""
    seen_files = {"file1.txt", "dir/file2.txt"}
    assert _is_safe_link_target("file1.txt", seen_files, "link.txt")


def test_safe_link_target_to_nested_file():
    """Test link targeting an existing nested file."""
    seen_files = {"file1.txt", "dir/file2.txt"}
    assert _is_safe_link_target("dir/file2.txt", seen_files, "link.txt")


def test_unsafe_link_target_directory_traversal():
    """Test link with directory traversal."""
    seen_files = {"file1.txt"}
    assert not _is_safe_link_target("../file.txt", seen_files, "link.txt")


def test_unsafe_link_target_self_reference():
    """Test self-referential link."""
    seen_files = {"file1.txt"}
    assert not _is_safe_link_target("file1.txt", seen_files, "file1.txt")


def test_unsafe_link_target_nonexistent():
    """Test link to nonexistent file."""
    seen_files = {"file1.txt"}
    assert not _is_safe_link_target("nonexistent.txt", seen_files, "link.txt")


# Unit Tests: Safe Extractall
def test_safe_extractall_creates_directory():
    """Test directory creation in safe_extractall."""
    tar_mock = Mock(spec=tarfile.TarFile)
    tar_mock.getmembers.return_value = []
    dest = Path("test_dir")

    with patch.object(Path, "mkdir") as mkdir_mock:
        _safe_extractall(tar_mock, dest)
        mkdir_mock.assert_called_once_with(parents=True, exist_ok=True)


def test_safe_extractall_blocks_directory_traversal():
    """Test that _safe_extractall prevents directory traversal via file paths."""
    tar_mock = Mock(spec=tarfile.TarFile)
    escaping_file = Mock(spec=tarfile.TarInfo)
    escaping_file.name = "../outside.txt"
    tar_mock.getmembers.return_value = [escaping_file]

    extracted_files = []

    def mock_extract(member, path):
        extracted_files.append(member.name)

    tar_mock.extract = mock_extract

    _safe_extractall(tar_mock, "test_dir")
    assert "../outside.txt" not in extracted_files


# Integration Tests: Tar Member Processing
def test_tar_extraction_single_file():
    """Test extracting a single file from tar."""
    files = {"file1.txt": b"content1"}
    with create_test_tar(files) as tar:
        members = list(_get_stripped_tar_members(tar))
        paths = {Path(m.name).as_posix() for m in members}
        assert paths == {"file1.txt"}


def test_tar_extraction_nested_files():
    """Test extracting nested files from tar."""
    files = {"subdir/file2.txt": b"content2", "subdir/": None}
    with create_test_tar(files) as tar:
        members = list(_get_stripped_tar_members(tar))
        paths = {Path(m.name).as_posix() for m in members}
        assert paths == {"subdir/file2.txt"}


def test_empty_tar_raises_error():
    """Test that empty tar raises appropriate error."""
    with create_test_tar({}) as tar:
        with pytest.raises(NotADirectoryError, match="Empty archive"):
            list(_get_stripped_tar_members(tar))


def test_invalid_tar_structure_raises_error():
    """Test that invalid tar structure raises appropriate error."""
    tar_buffer = BytesIO()
    with tarfile.open(fileobj=tar_buffer, mode="w:gz") as tar:
        info = tarfile.TarInfo("file.txt")
        info.type = tarfile.REGTYPE
        info.size = 0
        tar.addfile(info)

    tar_buffer.seek(0)
    with tarfile.open(fileobj=tar_buffer, mode="r:gz") as tar:
        with pytest.raises(NotADirectoryError, match="Cannot strip directory prefix"):
            list(_get_stripped_tar_members(tar))


# Integration Tests: Symlink Processing
def test_regular_symlink_processing():
    """Test handling of a regular symlink."""
    files = {"file1.txt": b"target content"}
    symlinks = {"link1.txt": "file1.txt"}

    with create_test_tar(files, symlinks) as tar:
        members = list(_get_stripped_tar_members(tar))
        links = {Path(m.name).as_posix(): m for m in members if m.islnk() or m.issym()}
        assert "link1.txt" in links
        assert Path(links["link1.txt"].linkname).as_posix() == "file1.txt"


def test_unsafe_symlink_conversion():
    """Test handling of symlink with parent reference."""
    files = {"file1.txt": b"content"}
    symlinks = {"link2.txt": "../file1.txt"}

    with create_test_tar(files, symlinks) as tar:
        members = list(_get_stripped_tar_members(tar))
        regular_files = {Path(m.name).as_posix(): m for m in members if m.isfile()}
        assert "link2.txt" in regular_files
        assert regular_files["link2.txt"].type == tarfile.REGTYPE


def test_circular_symlink_handling():
    """Test handling of circular symlink reference."""
    files = {}
    symlinks = {"circular.txt": "circular.txt"}

    with create_test_tar(files, symlinks) as tar:
        members = list(_get_stripped_tar_members(tar))
        regular_files = {Path(m.name).as_posix(): m for m in members if m.isfile()}
        assert "circular.txt" in regular_files
        assert regular_files["circular.txt"].type == tarfile.REGTYPE


# Integration Tests: Complex Scenarios
def test_symlink_chain_safety():
    """Test safety of complex symlink chains."""
    files = {"file1.txt": b"content1", "dir1/": None, "dir1/file2.txt": b"content2"}
    symlinks = {"dir1/link1.txt": "../file1.txt", "dir1/link2.txt": "link1.txt"}

    with create_test_tar(files, symlinks) as tar:
        members = list(_get_stripped_tar_members(tar))
        for member in members:
            if member.islnk() or member.issym():
                normalized_link = Path(member.linkname).as_posix()
                assert not normalized_link.startswith("..")


# Version-Specific Tests
@pytest.mark.skipif(sys.version_info >= (3, 12), reason="pre-3.12 test")
def test_extract_exec_uses_safe_extractall():
    """Test pre-3.12 extraction uses safe_extractall."""
    with TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        tar_path = temp_path / "test.tar.gz"

        with tarfile.open(tar_path, "w:gz") as tar:
            info = tarfile.TarInfo("testdir/file1.txt")
            info.size = len(b"content1")
            tar.addfile(info, BytesIO(b"content1"))

        extract_dir = temp_path / "extract_safe"
        with patch("gvsbuild.utils.base_expanders._safe_extractall") as safe_mock:
            extract_exec(tar_path, extract_dir)
            assert safe_mock.called


@pytest.mark.skipif(sys.version_info < (3, 12), reason="Python 3.12+ test")
def test_extract_exec_uses_data_filter():
    """Test Python 3.12+ extraction uses data_filter."""
    with TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        tar_path = temp_path / "test.tar.gz"

        with tarfile.open(tar_path, "w:gz") as tar:
            info = tarfile.TarInfo("testdir/file1.txt")
            info.size = len(b"content1")
            tar.addfile(info, BytesIO(b"content1"))

        extract_dir = temp_path / "extract_filter"
        with patch.object(tarfile, "data_filter") as filter_mock:
            extract_exec(tar_path, extract_dir)
            assert filter_mock.called


# End-to-End Tests
def test_extract_exe(temp_workspace):
    """Test extracting an exe file."""
    extract_dir = temp_workspace / "extract_exe"
    assert extract_exec(temp_workspace / "test.exe", extract_dir)
    assert (extract_dir / "test.exe").is_file()


def test_extract_zip_strip_one(temp_workspace):
    """Test extracting a zip file with strip_one."""
    extract_dir = temp_workspace / "extract_zip_strip"
    assert extract_exec(temp_workspace / "test.zip", extract_dir, strip_one=True)
    assert (extract_dir / "file1.txt").is_file()
    assert (extract_dir / "subdir" / "file2.txt").is_file()


def test_extract_tar_strip_one(temp_workspace):
    """Test extracting a tar file with strip_one."""
    extract_dir = temp_workspace / "extract_tar_strip"
    assert extract_exec(temp_workspace / "test.tar.gz", extract_dir, strip_one=True)
    assert (extract_dir / "file1.txt").is_file()
    assert (extract_dir / "subdir" / "file2.txt").is_file()


def test_extract_with_check_file(temp_workspace):
    """Test extraction with check_file parameter."""
    extract_dir = temp_workspace / "extract_check"
    check_file = temp_workspace / "check.txt"
    check_file.touch()
    assert not extract_exec(
        temp_workspace / "test.exe", extract_dir, check_file=check_file
    )
