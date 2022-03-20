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

from pathlib import Path

from gvsbuild.utils.base_expanders import Tarball
from gvsbuild.utils.base_project import Project, project_add


@project_add
class Pycairo(Tarball, Project):
    def __init__(self):
        Project.__init__(
            self,
            "pycairo",
            archive_url="https://github.com/pygobject/pycairo/releases/download/v1.21.0/pycairo-1.21.0.tar.gz",
            hash="251907f18a552df938aa3386657ff4b5a4937dde70e11aa042bc297957f4b74b",
            dependencies=["cairo", "python"],
            patches=[
                "pycairo_py3_8_load_dll.patch",
            ],
        )

    def build(self):
        cairo_inc = Path(self.builder.gtk_dir) / "include" / "cairo"
        self.builder.mod_env("INCLUDE", str(cairo_inc))
        self.exec_vs(r"%(python_dir)s\python.exe -m build")
        dist_dir = Path(self.build_dir) / "dist"
        for path in dist_dir.rglob("*.whl"):
            self.exec_vs(r"%(python_dir)s\python.exe -m pip install " + str(path))
        if self.builder.opts.py_wheel:
            self.install_dir("dist", "python")
        self.install(r".\COPYING share\doc\pycairo")
        self.install(r".\COPYING-LGPL-2.1 share\doc\pycairo")
        self.install(r".\COPYING-MPL-1.1 share\doc\pycairo")
