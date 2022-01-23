#  Copyright (C) 2016 - Yevgen Muntyan
#  Copyright (C) 2016 - Ignacio Casal Quinteiro
#  Copyright (C) 2016 - Arnavion
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

from gvsbuild.utils.base_expanders import Tarball
from gvsbuild.utils.base_project import Project, project_add


@project_add
class Pycairo(Tarball, Project):
    def __init__(self):
        Project.__init__(
            self,
            "pycairo",
            archive_url="https://github.com/pygobject/pycairo/releases/download/v1.20.1/pycairo-1.20.1.tar.gz",
            hash="1ee72b035b21a475e1ed648e26541b04e5d7e753d75ca79de8c583b25785531b",
            dependencies=["cairo", "python"],
            patches=[
                "pycairo_py3_8_load_dll.patch",
            ],
        )

    def build(self):
        cairo_inc = os.path.join(self.builder.gtk_dir, "include", "cairo")
        self.builder.mod_env("INCLUDE", cairo_inc)
        self.push_location(self.build_dir)
        self.exec_vs(r"%(python_dir)s\python.exe setup.py install")
        if self.builder.opts.py_egg:
            self.exec_vs(r"%(python_dir)s\python.exe setup.py bdist_egg")
        if self.builder.opts.py_wheel:
            self.exec_vs(r"%(python_dir)s\python.exe setup.py bdist_wheel")
        if self.builder.opts.py_egg or self.builder.opts.py_wheel:
            self.install_dir("dist", "python")
        self.install(r".\COPYING share\doc\pycairo")
        self.install(r".\COPYING-LGPL-2.1 share\doc\pycairo")
        self.install(r".\COPYING-MPL-1.1 share\doc\pycairo")
        self.install_pc_files()
        self.pop_location()
