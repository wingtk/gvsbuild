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

"""Default groups of projects."""

from .utils.base_group import Group, group_add


@group_add
class GroupTools(Group):
    def __init__(self):
        Group.__init__(
            self,
            "tools",
            dependencies=[
                "cargo",
                "cmake",
                "go",
                "meson",
                "msys2",
                "nasm",
                "ninja",
                "perl",
            ],
        )


@group_add
class GroupGtk3Full(Group):
    def __init__(self):
        Group.__init__(
            self,
            "gtk3-full",
            dependencies=[
                "adwaita-icon-theme",
                "clutter",
                "emeus",
                "gtk3",
                "gtksourceview4",
                "hicolor-icon-theme",
                "wing",
            ],
        )


@group_add
class GroupToolsCheck(Group):
    """Group to use all the tools handled by the script, to see at a glance if
    everything seems ok after (big) changes on the tools."""

    def __init__(self):
        Group.__init__(
            self,
            "tools-check",
            dependencies=[
                "lmdb",
                "x264",
                "libjpeg-turbo",
            ],
        )


@group_add
class GroupAll(Group):
    def __init__(self):
        Group.__init__(self, "all")
