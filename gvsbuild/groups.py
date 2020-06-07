#  Copyright (C) 2016 - Yevgen Muntyan
#  Copyright (C) 2016 - Ignacio Casal Quinteiro
#  Copyright (C) 2016 - Arnavion
#  Copyright (C) 2017 - Daniele Forghieri
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
Default groups of projects
"""

from .utils.base_group import Group, group_add
from .utils.base_project import Project, GVSBUILD_PROJECT

@group_add
class Group_Tools(Group):
    def __init__(self):
        Group.__init__(self,
            'tools',
            dependencies = [
                'cargo',
                'cmake',
                'go',
                'meson',
                'msys2',
                'nasm',
                'ninja',
                'nuget',
                'perl',
                'python',
                'yasm',
                ],
            )

@group_add
class Group_Gtk3_Full(Group):
    '''
    Base gtk/gtk3 projects
    '''
    def __init__(self):
        Group.__init__(self,
            'gtk3-full',
            dependencies = [
                'adwaita-icon-theme',
                'clutter',
                'emeus',
                'graphene',
                'gsettings-desktop-schemas',
                'gtk3',
                'gtksourceview3',
                'hicolor-icon-theme',
                'wing',
                ],
            )

@group_add
class Group_Gtk3_Extra(Group):
    '''
    Gtk extra projects: gstreamer, network, ...
    '''
    def __init__(self):
        Group.__init__(self,
            'gtk3-extra',
            dependencies = [
                'enchant',
                'glib-networking',
                'glib-openssl',
                'gst-plugins-bad',
                'gst-plugins-base',
                'gst-plugins-good',
                'gst-python',
                'gstreamer',
                'pygobject',
                'libgxps',
                ],
            )

@group_add
class Group_Script_Extra(Group):
    '''
    Project not belonging directly to the gtk ones, used for the ci integration
    '''
    def __init__(self):
        Group.__init__(self,
            'script-extra',
            dependencies = [
                'enchant',
                'dcv-color-primitives',
                'cyrus-sasl',
                'ffmpeg',
                'grpc',
                'protobuf-c',
                'json-c',
                'leveldb',
                'lgi',
                'libcurl',
                'libmicrohttpd',
                'libsoup',
                'libssh',
                'libssh2',
                'libuv',
                'libyuv',
                'libzip',
                'luajit',
                'portaudio',
                'quiche',
                'x264',
                ],
            )

@group_add
class Group_Tools_Check(Group):
    '''
    Group to use all the tools handled by the script, to see at a glance if everything
    seems ok after (big) changes on the tools
    '''
    def __init__(self):
        Group.__init__(self,
            'tools-check',
            dependencies = [
                'lmdb',
                'x264',
                'libjpeg-turbo',
                'grpc',
                ],
            )

@group_add
class Group_All(Group):
    def __init__(self):
        all_prj = [x.name for x in Project._projects if x.type == GVSBUILD_PROJECT]
        Group.__init__(self,
            'all',
            dependencies = all_prj
        )
