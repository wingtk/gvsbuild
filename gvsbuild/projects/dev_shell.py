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

from gvsbuild.utils.base_project import Project, ProjectType, project_add
from gvsbuild.utils.simple_ui import log


@project_add
class DevShell(Project):
    def __init__(self):
        Project.__init__(
            self,
            "dev-shell",
            # We may need all tools
            dependencies=["tools"],
            version="0.1.0",
            # We don't want this project to be built with the group 'all'
            type=ProjectType.IGNORE,
        )
        self.meson = True

    def unpack(self):
        # Nothing to do, it's not really a project
        pass

    def export(self):
        # Nothing to do, it's not really a project
        pass

    def finalize_dep(self, builder, deps):
        if builder.opts.skip:
            for s in builder.opts.skip:
                p = Project.get_project(s)
                if p in deps:
                    log.log(f"dev-shell: skip {s}")
                    deps.remove(p)
                    if s in ["meson", "python"]:
                        # We disable the meson management
                        self.meson = False

    def build(self):
        # Do the shell
        print("")
        print("gvsbuild dev shell. Type exit to exit :)")
        print("")
        print("The environment var GTK_BASE_DIR points to the gtk installation dir")
        print(f"({self.builder.gtk_dir})")
        print("if you need it e.g. as a --prefix option")
        print("")
        if self.meson:
            # Add a _meson env to use it directly
            meson_path = Project.get_tool_path("meson")
            self.builder.mod_env("_MESON", f"python {meson_path}\\meson.py")
            print("If you need to use meson you can use the _MESON environment, e.g.")
            print("%_MESON% configure")
            print("")

        # If you need to use it as a --prefix in some build test ...
        self.builder.mod_env("GTK_BASE_DIR", self.builder.gtk_dir)
        self.builder.mod_env("PROMPT", "[ gvsbuild shell ] $P $G", subst=True)
        self.builder.exec_vs("cmd", working_dir=self.builder.working_dir)
