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
import sys
from pathlib import Path

from gvsbuild.utils.base_builders import Meson
from gvsbuild.utils.base_expanders import Tarball
from gvsbuild.utils.base_project import Project, project_add
from gvsbuild.utils.simple_ui import log
from gvsbuild.utils.utils import python_find_libs_dir


@project_add
class GObjectIntrospection(Tarball, Meson):
    def __init__(self):
        Project.__init__(
            self,
            "gobject-introspection",
            version="1.76.1",
            lastversion_even=True,
            repository="https://gitlab.gnome.org/GNOME/gobject-introspection",
            archive_url="https://download.gnome.org/sources/gobject-introspection/{major}.{minor}/gobject-introspection-{version}.tar.xz",
            hash="196178bf64345501dcdc4d8469b36aa6fe80489354efe71cb7cb8ab82a3738bf",
            dependencies=[
                "ninja",
                "meson",
                "msys2",
                "pkgconf",
                "glib",
            ],
            # https://gitlab.gnome.org/GNOME/gobject-introspection/-/issues/427
            patches=["incorrect-giscanner-path.patch"],
        )

    def build(self):
        # For finding gobject-introspection.pc
        self.builder.mod_env("PKG_CONFIG_PATH", ".")
        # For finding & using girepository.lib/.dll
        self.builder.mod_env("LIB", r".\girepository")
        self.builder.mod_env("PATH", r".\girepository")
        # For linking the _giscanner.pyd extension module when using a virtualenv
        py_dir = Path(sys.executable).parent
        py_libs = python_find_libs_dir(py_dir)
        if py_libs:
            log.debug(f"Python library path is [{py_libs}]")
            self.builder.mod_env("LIB", py_libs, prepend=False)

        Meson.build(
            self,
            meson_params="-Dpython=%s\\python.exe -Dcairo_libname=cairo-gobject-2.dll"
            % (py_dir,),
        )
