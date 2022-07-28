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
class PyGObject(Tarball, Project):
    def __init__(self):
        Project.__init__(
            self,
            "pygobject",
            archive_url="https://download.gnome.org/sources/pygobject/3.42/pygobject-3.42.2.tar.xz",
            hash="ade8695e2a7073849dd0316d31d8728e15e1e0bc71d9ff6d1c09e86be52bc957",
            dependencies=["python", "pycairo", "gobject-introspection", "libffi"],
            patches=[
                "pygobject_py3_8_load_dll.patch",
            ],
        )

    def build(self):
        gtk_dir = self.builder.gtk_dir
        add_inc = [
            str(Path(gtk_dir) / "include" / "cairo"),
            str(Path(gtk_dir) / "include" / "gobject-introspection-1.0"),
            str(Path(gtk_dir) / "include" / "glib-2.0"),
            str(Path(gtk_dir) / "lib" / "glib-2.0" / "include"),
        ]
        self.builder.mod_env("INCLUDE", ";".join(add_inc))
        self.exec_vs(r"%(python_dir)s\python.exe -m build")
        dist_dir = Path(self.build_dir) / "dist"
        for path in dist_dir.rglob("*.whl"):
            self.exec_vs(
                r"%(python_dir)s\python.exe -m pip install --force-reinstall "
                + str(path)
            )
        if self.builder.opts.py_wheel:
            self.install_dir("dist", "python")
        self.install(r".\COPYING share\doc\pygobject")
