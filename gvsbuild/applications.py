#  Copyright (C) 2016 - Yevgen Muntyan
#  Copyright (C) 2016 - Ignacio Casal Quinteiro
#  Copyright (C) 2016 - Arnavion
#  Copyright (C) 2020 - Daniel F. Dickinson
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
Default apps to build
"""

import os
import glob
import shutil

from .utils.simple_ui import log
from .utils.utils import convert_to_msys
from .utils.utils import file_replace
from .utils.utils import python_find_libs_dir
from .utils.base_expanders import Tarball, GitRepo
from .utils.base_expanders import NullExpander
from .utils.base_application import Application, application_add
from .utils.base_project import Project
from .utils.base_project import GVSBUILD_IGNORE
from .utils.base_builders import Meson, MercurialCmakeProject, CmakeProject, Rust


@application_add
class Application_zim_desktop_wiki(GitRepo, Project):
    def __init__(self):
        GitRepo.__init__(self)
        Application.__init__(self,
            'zim-desktop-wiki',
            repo_url = 'https://github.com/zim-desktop-wiki/zim-desktop-wiki',
            fetch_submodules = False,
            tag = '0.73.2',
            dependencies = [
                'adwaita-icon-theme',
                'python',
                'gtksourceview3',
                'gtk3',
                'hicolor-icon-theme',
                'pygobject'
            ],
            enable_gi = True, )

    def build(self):
        pass
