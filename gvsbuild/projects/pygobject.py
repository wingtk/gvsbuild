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
class PyGObject(Tarball, Project):
    def __init__(self):
        Project.__init__(
            self,
            "pygobject",
            archive_url="https://download.gnome.org/sources/pygobject/3.42/pygobject-3.42.0.tar.xz",
            hash="9b12616e32cfc792f9dc841d9c472a41a35b85ba67d3a6eb427e307a6fe4367b",
            dependencies=["python", "pycairo", "gobject-introspection", "libffi"],
            patches=[
                "pygobject_py3_8_load_dll.patch",
            ],
        )

    def build(self):
        gtk_dir = self.builder.gtk_dir
        add_inc = [
            os.path.join(gtk_dir, "include", "cairo"),
            os.path.join(gtk_dir, "include", "gobject-introspection-1.0"),
            os.path.join(gtk_dir, "include", "glib-2.0"),
            os.path.join(gtk_dir, "lib", "glib-2.0", "include"),
        ]
        self.builder.mod_env("INCLUDE", ";".join(add_inc))
        self.push_location(self.build_dir)
        self.exec_vs(r"%(python_dir)s\python.exe setup.py install")
        if self.builder.opts.py_egg:
            self.exec_vs(r"%(python_dir)s\python.exe setup.py bdist_egg")
        if self.builder.opts.py_wheel:
            self.exec_vs(r"%(python_dir)s\python.exe setup.py bdist_wheel")
        if self.builder.opts.py_egg or self.builder.opts.py_wheel:
            self.install_dir("dist", "python")
        self.install(r".\COPYING share\doc\pygobject")
        self.install(r".\gi\pygobject.h include\pygobject-3.0")
        self.install_pc_files()
        self.pop_location()
