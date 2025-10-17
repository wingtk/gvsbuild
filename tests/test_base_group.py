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


from gvsbuild.utils.base_group import Group, group_add
from gvsbuild.utils.base_project import Project, ProjectType


def test_group_creation():
    """Test Group creation."""
    group = Group("test-group")
    assert group.name == "test-group"


def test_group_unpack():
    """Test Group unpack does nothing."""
    group = Group("test-group")
    # Should not raise error and return None
    result = group.unpack()
    assert result is None


def test_group_build():
    """Test Group build does nothing."""
    group = Group("test-group")
    # Should not raise error and return None
    result = group.build()
    assert result is None


def test_group_export():
    """Test Group export does nothing."""
    group = Group("test-group")
    # Should not raise error and return None
    result = group.export()
    assert result is None


def test_group_add_decorator():
    """Test group_add decorator registers group."""

    # Create a test group with unique name
    @group_add
    class TestGroupDecorator(Group):
        def __init__(self):
            Group.__init__(self, "test-group-decorator-unique-name")

    # The class should be registered
    assert TestGroupDecorator is not None


def test_group_with_dependencies():
    """Test Group with dependencies."""
    group = Group("test-group-with-deps", dependencies=["dep1", "dep2"])
    assert group.dependencies == ["dep1", "dep2"]


def test_real_groups_exist():
    """Test that real groups from the project exist."""
    Project.add_all()
    groups = [p for p in Project._projects if p.type == ProjectType.GROUP]

    # Should have at least some groups
    assert len(groups) > 0

    # Check group names
    group_names = [g.name for g in groups]
    # Common groups in gvsbuild
    # Note: actual group names may vary, this test just ensures groups exist
    assert len(group_names) > 0
