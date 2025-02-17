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
import tarfile
import zipfile
from collections.abc import Iterator
from contextlib import contextmanager
from io import BytesIO
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

from gvsbuild.utils.base_expanders import (
    __get_stripped_tar_members,
    __is_safe_link_target,
    __is_unsafe_path,
    __strip_path,
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


def test_strip_path():
    """Test the path stripping functionality."""
    assert __strip_path("testdir/file.txt") == "file.txt"
    assert __strip_path("testdir/subdir/file.txt") == "subdir/file.txt"
    assert __strip_path("file.txt") is None
    assert __strip_path("testdir") is None


def test_is_safe_link_target():
    """Test the link target safety checker."""
    seen_files = {"file1.txt", "dir/file2.txt"}

    # Safe cases
    assert __is_safe_link_target("file1.txt", seen_files, "link.txt")
    assert __is_safe_link_target("dir/file2.txt", seen_files, "link.txt")

    # Unsafe cases
    assert not __is_safe_link_target("../file.txt", seen_files, "link.txt")
    assert not __is_safe_link_target(
        "file1.txt", seen_files, "file1.txt"
    )  # Self-reference
    assert not __is_safe_link_target("nonexistent.txt", seen_files, "link.txt")


def test_basic_tar_extraction():
    """Test basic tar extraction without symlinks."""
    files = {"file1.txt": b"content1", "subdir/file2.txt": b"content2", "subdir/": None}

    with create_test_tar(files) as tar:
        members = list(__get_stripped_tar_members(tar))

        # Check paths are stripped and normalized
        paths = {Path(m.name).as_posix() for m in members}
        assert paths == {"file1.txt", "subdir/file2.txt"}


def test_symlink_handling():
    """Test handling of various symlink scenarios."""
    files = {
        "file1.txt": b"target content",
        "subdir/file2.txt": b"content2",
        "subdir/": None,
    }
    symlinks = {
        "link1.txt": "file1.txt",  # Regular symlink
        "link2.txt": "../file1.txt",  # Symlink with parent reference
        "circular.txt": "circular.txt",  # Circular reference
    }

    with create_test_tar(files, symlinks) as tar:
        members = list(__get_stripped_tar_members(tar))

        # Find the processed symlinks
        links = {Path(m.name).as_posix(): m for m in members if m.islnk() or m.issym()}
        regular_files = {Path(m.name).as_posix(): m for m in members if m.isfile()}

        # Regular symlink should be preserved
        assert "link1.txt" in links
        assert Path(links["link1.txt"].linkname).as_posix() == "file1.txt"

        # Parent reference should be converted to regular file
        assert "link2.txt" in regular_files
        assert regular_files["link2.txt"].type == tarfile.REGTYPE

        # Circular reference should be converted to regular file
        assert "circular.txt" in regular_files
        assert regular_files["circular.txt"].type == tarfile.REGTYPE


def test_empty_tar():
    """Test handling of empty tar files."""
    with create_test_tar({}) as tar:
        with pytest.raises(NotADirectoryError, match="Empty archive"):
            list(__get_stripped_tar_members(tar))


def test_invalid_tar_structure():
    """Test handling of tar files with invalid structure."""
    tar_buffer = BytesIO()
    with tarfile.open(fileobj=tar_buffer, mode="w:gz") as tar:
        info = tarfile.TarInfo("file.txt")
        info.type = tarfile.REGTYPE
        info.size = 0
        tar.addfile(info)

    tar_buffer.seek(0)
    with tarfile.open(fileobj=tar_buffer, mode="r:gz") as tar:
        with pytest.raises(NotADirectoryError, match="Cannot strip directory prefix"):
            list(__get_stripped_tar_members(tar))


def test_complex_symlink_chain():
    """Test handling of complex symlink chains."""
    files = {
        "file1.txt": b"content1",
        "dir1/": None,
        "dir1/file2.txt": b"content2",
        "dir2/": None,
        "dir2/subdir/": None,
    }
    symlinks = {
        "dir1/link1.txt": "../file1.txt",
        "dir2/link2.txt": "../dir1/link1.txt",
        "dir2/subdir/link3.txt": "../link2.txt",
    }

    with create_test_tar(files, symlinks) as tar:
        members = list(__get_stripped_tar_members(tar))

        # All symlinks should either be converted to files or have safe targets
        for member in members:
            if member.islnk() or member.issym():
                normalized_link = Path(member.linkname).as_posix()
                assert not normalized_link.startswith("..")
                assert normalized_link in {Path(m.name).as_posix() for m in members}


def test_is_unsafe_path():
    """Test path safety checking."""
    # Safe paths
    assert not __is_unsafe_path("file.txt")
    assert not __is_unsafe_path("dir/file.txt")

    # Unsafe paths
    assert __is_unsafe_path("C:/file.txt")  # Windows absolute
    assert __is_unsafe_path("../file.txt")  # Directory traversal
    assert __is_unsafe_path("dir/../file.txt")  # Directory traversal


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


def test_extract_exe(temp_workspace):
    """Test extracting an exe file."""
    extract_dir = temp_workspace / "extract_exe"
    assert extract_exec(temp_workspace / "test.exe", extract_dir)
    assert (extract_dir / "test.exe").is_file()


def test_extract_exe_with_dir_part(temp_workspace):
    """Test extracting an exe file with dir_part."""
    extract_dir = temp_workspace / "extract_dir_part"
    assert extract_exec(temp_workspace / "test.exe", extract_dir, dir_part="subdir")
    assert (extract_dir / "subdir" / "test.exe").is_file()


def test_extract_zip_normal(temp_workspace):
    """Test extracting a zip file without stripping."""
    extract_dir = temp_workspace / "extract_zip"
    assert extract_exec(temp_workspace / "test.zip", extract_dir)
    assert (extract_dir / "basedir" / "file1.txt").is_file()
    assert (extract_dir / "basedir" / "subdir" / "file2.txt").is_file()


def test_extract_zip_strip_one(temp_workspace):
    """Test extracting a zip file with strip_one."""
    extract_dir = temp_workspace / "extract_zip_strip"
    assert extract_exec(temp_workspace / "test.zip", extract_dir, strip_one=True)
    assert (extract_dir / "file1.txt").is_file()
    assert (extract_dir / "subdir" / "file2.txt").is_file()


def test_extract_tar_normal(temp_workspace):
    """Test extracting a tar file without stripping."""
    extract_dir = temp_workspace / "extract_tar"
    assert extract_exec(temp_workspace / "test.tar.gz", extract_dir)
    assert (extract_dir / "basedir" / "file1.txt").is_file()
    assert (extract_dir / "basedir" / "subdir" / "file2.txt").is_file()


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
