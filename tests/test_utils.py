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
import os

import pytest

from gvsbuild.utils.utils import (
    convert_to_msys,
    file_replace,
    ordered_set,
    python_find_libs_dir,
    read_file,
    rmtree_full,
    write_file,
)


def test_convert_to_msys():
    """Test converting Windows paths to MSYS format."""
    result = convert_to_msys("C:\\Users\\test")
    assert result == "/C/Users/test"

    result = convert_to_msys("D:\\Program Files")
    assert result == "/D/Program Files"


def test_convert_to_msys_invalid():
    """Test converting invalid path raises error."""
    with pytest.raises(NotADirectoryError):
        convert_to_msys("/invalid/path")


def test_read_write_file(tmp_path):
    """Test reading and writing files."""
    test_file = tmp_path / "test.txt"
    content = ["line1", "line2", "line3"]

    # Write file
    write_file(test_file, content)
    assert test_file.exists()

    # Read file
    result = read_file(test_file)
    assert result == content


def test_file_replace(tmp_path):
    """Test file replacement functionality."""
    test_file = tmp_path / "replace.txt"
    original_content = ["Hello World", "Python is great", "Hello Python"]
    write_file(test_file, original_content)

    # Replace "Hello" with "Hi"
    file_replace(test_file, [("Hello", "Hi")])

    result = read_file(test_file)
    assert result == ["Hi World", "Python is great", "Hi Python"]

    # Backup file should exist
    backup_file = tmp_path / "replace.txt.bak"
    assert backup_file.exists()


def test_file_replace_no_backup(tmp_path):
    """Test file replacement without backup."""
    test_file = tmp_path / "replace2.txt"
    original_content = ["foo bar"]
    write_file(test_file, original_content)

    file_replace(test_file, [("foo", "baz")], make_bak=False)

    result = read_file(test_file)
    assert result == ["baz bar"]

    # Backup file should not exist
    backup_file = tmp_path / "replace2.txt.bak"
    assert not backup_file.exists()


def test_file_replace_no_changes(tmp_path):
    """Test file replacement with no matches."""
    test_file = tmp_path / "replace3.txt"
    original_content = ["foo bar"]
    write_file(test_file, original_content)

    file_replace(test_file, [("notfound", "replacement")])

    result = read_file(test_file)
    assert result == original_content


def test_file_replace_regex(tmp_path):
    """Test file replacement with regex."""
    test_file = tmp_path / "replace4.txt"
    original_content = ["value=123", "value=456"]
    write_file(test_file, original_content)

    file_replace(test_file, [(r"value=\d+", "value=999")])

    result = read_file(test_file)
    assert result == ["value=999", "value=999"]


def test_ordered_set():
    """Test ordered_set functionality."""
    os = ordered_set()

    # Add items
    os.add("first")
    os.add("second")
    os.add("third")

    # Check order is preserved
    items = list(os)
    assert items == ["first", "second", "third"]

    # Adding duplicate should not change order
    os.add("first")
    items = list(os)
    assert items == ["first", "second", "third"]


def test_ordered_set_remove():
    """Test ordered_set remove functionality."""
    os = ordered_set()
    os.add("a")
    os.add("b")
    os.add("c")

    os.remove("b")
    items = list(os)
    assert items == ["a", "c"]


def test_ordered_set_contains():
    """Test ordered_set membership test."""
    os = ordered_set()
    os.add("test")

    assert "test" in os
    assert "nothere" not in os


def test_rmtree_full(tmp_path):
    """Test rmtree_full functionality."""
    # Create directory with file
    test_dir = tmp_path / "test_rmtree"
    test_dir.mkdir()
    (test_dir / "file.txt").write_text("content")

    # Remove directory
    rmtree_full(str(test_dir))

    # Directory should not exist
    assert not test_dir.exists()


def test_rmtree_full_nonexistent(tmp_path):
    """Test rmtree_full with non-existent directory."""
    nonexistent = tmp_path / "doesnotexist"

    # Should not raise error
    rmtree_full(str(nonexistent))


def test_rmtree_full_readonly(tmp_path):
    """Test rmtree_full with read-only files."""
    test_dir = tmp_path / "test_readonly"
    test_dir.mkdir()
    test_file = test_dir / "readonly.txt"
    test_file.write_text("content")

    # Make file read-only
    os.chmod(test_file, 0o444)

    # Should still be able to remove
    rmtree_full(str(test_dir))
    assert not test_dir.exists()


def test_rmtree_full_with_retry(tmp_path):
    """Test rmtree_full with retry option."""
    test_dir = tmp_path / "test_retry"
    test_dir.mkdir()
    (test_dir / "file.txt").write_text("content")

    rmtree_full(str(test_dir), retry=True)
    assert not test_dir.exists()


def test_python_find_libs_dir_direct(tmp_path):
    """Test finding Python libs directory directly."""
    # Create fake Python directory with libs
    python_dir = tmp_path / "python"
    python_dir.mkdir()
    libs_dir = python_dir / "libs"
    libs_dir.mkdir()

    result = python_find_libs_dir(str(python_dir))
    assert result == str(libs_dir)


def test_python_find_libs_dir_virtualenv(tmp_path):
    """Test finding Python libs directory from virtualenv."""
    # Create fake virtualenv
    venv_dir = tmp_path / "venv"
    venv_dir.mkdir()

    # Create fake Python directory with libs
    python_dir = tmp_path / "python"
    python_dir.mkdir()
    libs_dir = python_dir / "libs"
    libs_dir.mkdir()

    # Create pyvenv.cfg pointing to python_dir
    pyvenv_cfg = venv_dir / "pyvenv.cfg"
    pyvenv_cfg.write_text(f"home = {python_dir}\n")

    result = python_find_libs_dir(str(venv_dir))
    assert result == str(libs_dir)


def test_python_find_libs_dir_not_found(tmp_path):
    """Test python_find_libs_dir when libs directory doesn't exist."""
    python_dir = tmp_path / "python"
    python_dir.mkdir()

    result = python_find_libs_dir(str(python_dir))
    # Should return path even if it doesn't exist, or None
    assert result is None or not os.path.isdir(result)
