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

from pathlib import Path

from gvsbuild.utils.base_builders import Meson
from gvsbuild.utils.base_expanders import Tarball
from gvsbuild.utils.base_project import Project, project_add


@project_add
class PyGObject(Tarball, Meson):
    def __init__(self):
        Project.__init__(
            self,
            "pygobject",
            version="3.46.0",
            lastversion_even=True,
            repository="https://gitlab.gnome.org/GNOME/pygobject",
            archive_url="https://download.gnome.org/sources/pygobject/{major}.{minor}/pygobject-{version}.tar.xz",
            hash="426008b2dad548c9af1c7b03b59df0440fde5c33f38fb5406b103a43d653cafc",
            dependencies=["pycairo", "gobject-introspection", "libffi"],
            patches=[
                "pygobject_py3_8_load_dll.patch",
            ],
        )

    def build(self):
        Meson.build(self)
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
