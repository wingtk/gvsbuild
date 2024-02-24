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

"""Base project class, used also for tools."""

import datetime
import os
import pathlib
import re
import shutil
from enum import Enum
from typing import Dict, Generic, List, Tuple, TypeVar

from .simple_ui import log
from .utils import _rmtree_error_handler


class ProjectType(str, Enum):
    IGNORE = "ignore"
    PROJECT = "project"
    TOOL = "tool"
    GROUP = "group"


class Options:
    def __init__(self):
        self.enable_gi = False
        self.enable_fips = False
        self.ffmpeg_enable_gpl = False
        self.verbose = False
        self.debug = False
        self.platform = "x64"
        self.configuration = "release"
        self.release_configuration_is_actually_debug_optimized = False
        self.build_dir = None
        self.archives_download_dir = None
        self.export_dir = None
        self.patches_root_dir = None
        self.tools_root_dir = None
        self.vs_ver = None
        self.vs_install_path = None
        self.win_sdk_ver = None
        self.net_target_framework = None
        self.net_target_framework_version = None
        self.msys_dir = None
        self.clean = False
        self.msbuild_opts = None
        self.use_env = False
        self.deps = False
        self.check_hash = False
        self.skip = False
        self.make_zip = False
        self.zip_continue = False
        self.from_scratch = False
        self.keep_tools = False
        self.fast_build = False
        self.keep_going = False
        self.clean_built = False
        self.py_wheel = False
        self.log_size = None
        self.log_single = False
        self.cargo_opts = None
        self.ninja_opts = None
        self.capture_out = False
        self.print_out = False
        self.git_expand_dir = None
        self.projects = None


P = TypeVar("P")


class Project(Generic[P]):
    def __init__(self, name, **kwargs):
        object.__init__(self)
        self.patch_dir = None
        self.build_dir = None
        self.pkg_dir = None
        self.builder = None
        self.name = name
        self.prj_dir = name
        self.dependencies = []
        self.patches = []
        self.archive_url = None
        self.archive_filename = None
        self.tarbomb = False
        self.type = None
        self.version = None
        self.repository = None
        self.lastversion_major = None
        self.lastversion_even = None
        self.internal = False
        self.mark_file = None
        self.clean = False
        self.to_add = True
        self.extra_env = {}
        self.tag = None
        self.repo_url = None
        self.archive_filename = None

        for k in kwargs:
            setattr(self, k, kwargs[k])
        self.__working_dir = None
        if len(self.name) > Project.name_len:
            Project.name_len = len(self.name)

        if not self.version:
            self.version = f"git/{self.tag}" if self.repo_url else "undefined"
        version_params = {
            "version": self.version,
            "tag": self.tag,
        }
        match = re.match(
            r"(?P<major>\d+)(\.(?P<minor>\d+))?(\.(?P<micro>\d+))?", self.version
        )
        if match:
            for param in ["major", "minor", "micro"]:
                version_params[param] = match[param] or ""

        if self.archive_url:
            self.archive_url = self.archive_url.format(**version_params)
        if self.archive_filename:
            self.archive_filename = self.archive_filename.format(**version_params)

        # register version params for use from derived classes
        self.version_params = version_params

    _projects: List[P] = []
    _names: List[str] = []
    _dict: Dict[str, P] = {}
    _ver_res = None
    name_len = 0
    # List of class/type to add, now not at import time but after some options are parsed
    _reg_prj_list: List[Tuple[P, ProjectType]] = []
    # build option
    opts = Options()

    @staticmethod
    def compute_dependencies(projects):
        global_deps = {p.name for p in projects}

        def _add_project_dependencies(project):
            for dep in project.dependencies:
                if dep not in global_deps:
                    global_deps.add(dep)
                    _add_project_dependencies(Project.get_project(dep))

        for project in projects:
            _add_project_dependencies(project)

        return [Project.get_project(p) for p in global_deps]

    def __str__(self):
        return self.name

    def __repr__(self):
        return repr(self.name)

    def load_defaults(self):
        # Used by the tools to load default paths/filenames
        pass

    def finalize_dep(self, builder, deps):
        """Used to manipulate the dependencies list, to add or remove projects
        For the dev-shell project is used to limit the tools to use."""
        pass

    def build(self):
        raise NotImplementedError("build")

    def post_install(self):
        pass

    def add_dependency(self, dep):
        self.dependencies.append(dep)

    def exec_cmd(self, cmd, working_dir=None, add_path=None):
        self.builder.exec_cmd(cmd, working_dir=working_dir, add_path=add_path)

    def exec_vs(self, cmd, add_path=None):
        self.builder.exec_vs(
            cmd, working_dir=self._get_working_dir(), add_path=add_path
        )

    def exec_msbuild(self, cmd, configuration=None, add_path=None):
        if not configuration:
            configuration = "%(configuration)s"
        self.exec_vs(
            "msbuild "
            + cmd
            + " /p:Configuration="
            + configuration
            + " %(msbuild_opts)s",
            add_path=add_path,
        )

    def _msbuild_make_search_replace(self, org_platform):
        """Return the search & replace strings (converted to bytes to update
        the platform Toolset version (v140, v141, ...) to use a new compiler,
        e.g. to use vs2017 solution's files for vs2019.

        The '<PlatformToolset' at the beginning is missing to handle
        projects like libmictohttpd that has a condition in the platform
        definition
        """

        ver = self.builder.opts.vs_ver
        if ver == "15":
            dst_platform = "141"
        elif ver == "16":
            dst_platform = "142"
        elif ver == "17":
            dst_platform = "143"
        else:
            dst_platform = f"{ver}0"
        search = (">v%u</PlatformToolset>" % (org_platform,)).encode("utf-8")
        replace = f">v{dst_platform}</PlatformToolset>".encode()

        return search, replace

    def _msbuild_copy_dir(self, dst, src, search, replace):
        """Converts & copy a directory of a vs solution to be use with a new
        platform toolset & visual studio version.

        If dst is None the change is made in place
        """

        if dst:
            os.makedirs(dst, exist_ok=True)
            copy = True
        else:
            dst = src
            copy = False

        for cf in os.scandir(src):
            src_full = os.path.join(src, cf.name)
            dst_full = os.path.join(dst, cf.name)

            if cf.is_file():
                with open(src_full, "rb") as f:
                    content = f.read()
                new_content = content.replace(search, replace)
                if content != new_content:
                    log.info(f"File changed ({src_full})")
                    write = True
                else:
                    log.info(f"   same file ({src_full})")
                    write = copy

                if write:
                    dst_full = os.path.join(dst, cf.name)
                    with open(dst_full, "wb") as f:
                        f.write(new_content)
            elif cf.is_dir():
                self._msbuild_copy_dir(
                    dst_full if copy else None, src_full, search, replace
                )

    def exec_msbuild_gen(
        self,
        base_dir,
        sln_file,
        add_pars="",
        configuration=None,
        add_path=None,
        use_env=False,
    ):
        r"""looks for base_dir\{vs_ver}\sln_file or
        base_dir\{vs_ver_tear}\sln_file for launching the msbuild commamd.

        If it's not present in the directory the system start to look
        backward to find the first version present
        """

        def _msbuild_ok(self, dir_part):
            full = os.path.join(self.build_dir, base_dir, dir_part, sln_file)
            log.info(f"Checking for '{full}'")
            return os.path.exists(full)

        def _msbuild_copy(self, org_path, org_platform, use_ver=True):
            if use_ver:
                dst_part = f"vs{self.builder.opts.vs_ver}"
            else:
                dst_part = self.builder.vs_ver_year
            dst = os.path.join(self.build_dir, base_dir, dst_part)
            src = os.path.join(self.build_dir, base_dir, org_path)
            search, replace = self._msbuild_make_search_replace(org_platform)
            log.info(f"Vs solution copy: '{src}' -> '{dst}'")
            self._msbuild_copy_dir(dst, src, search, replace)
            return dst_part

        part = f"vs{self.builder.opts.vs_ver}"
        if not _msbuild_ok(self, part):
            part = self.builder.vs_ver_year
            if not _msbuild_ok(self, part):
                part = None

        if not part:
            look = {
                "12": [],
                "14": [
                    (
                        "vs12",
                        120,
                        True,
                    ),
                    (
                        "vs2013",
                        120,
                        False,
                    ),
                ],
                "15": [
                    (
                        "vs14",
                        140,
                        True,
                    ),
                    (
                        "vs2015",
                        140,
                        False,
                    ),
                    (
                        "vs12",
                        120,
                        True,
                    ),
                    (
                        "vs2013",
                        120,
                        False,
                    ),
                ],
                "16": [
                    (
                        "vs15",
                        141,
                        True,
                    ),
                    (
                        "vs2017",
                        141,
                        False,
                    ),
                    (
                        "vs14",
                        140,
                        True,
                    ),
                    (
                        "vs2015",
                        140,
                        False,
                    ),
                    (
                        "vs12",
                        120,
                        True,
                    ),
                    (
                        "vs2013",
                        120,
                        False,
                    ),
                ],
            }
            lst = look.get(self.builder.opts.vs_ver, [])
            for p in lst:
                if _msbuild_ok(self, p[0]):
                    # Found one, create the new directory with a copy, changing the platform identifier
                    part = _msbuild_copy(self, p[0], p[1], p[2])
                    break
            if part:
                # We log what we found because is not the default
                log.log(f"Project {self.name}, using {part} directory")

        if part:
            cmd = os.path.join(base_dir, part, sln_file)
            if add_pars:
                cmd += f" {add_pars}"
            if use_env:
                cmd += " /p:UseEnv=True"
        else:
            log.error_exit(
                f"Solution file '{sln_file}' for project '{self.name}' not found!"
            )
        self.exec_msbuild(cmd, configuration, add_path)
        return part

    def install(self, *args):
        self.builder.install(self._get_working_dir(), self.pkg_dir, *args)

    def install_dir(self, src, dest=None):
        if not dest:
            dest = os.path.basename(src)
        self.builder.install_dir(self._get_working_dir(), self.pkg_dir, src, dest)

    def install_pc_files(self, base_dir="pc-files"):
        """Install, setting dir & version, the .pc files."""
        pkgconfig_dir = os.path.join(self.pkg_dir, "lib", "pkgconfig")
        self.builder.make_dir(pkgconfig_dir)

        src_dir = os.path.join(self._get_working_dir(), base_dir)
        log.debug(f"Copy .pc files from {src_dir} to {pkgconfig_dir}")
        gtk_dir = self.builder.gtk_dir.replace("\\", "/")
        for f in os.scandir(src_dir):
            if f.is_file():
                log.debug(f" {f.name}")
                content = pathlib.Path(f.path).read_text()
                _t = content.replace("@prefix@", gtk_dir)
                content = _t
                _t = content.replace("@version@", self.version)
                content = _t

                with open(
                    os.path.join(pkgconfig_dir, f.name), "w", encoding="utf-8"
                ) as fo:
                    fo.write(content)

    def patch(self):
        for p in self.patches:
            name = os.path.basename(p)
            stamp = os.path.join(self.build_dir, f"{name}.patch-applied")
            if not os.path.exists(stamp):
                log.log(f"Applying patch {p}")
                self.builder.exec_msys(
                    ["patch", "-p1", "-i", p], working_dir=self._get_working_dir()
                )
                with open(stamp, "w", encoding="utf-8") as stampfile:
                    stampfile.write("done")
            else:
                log.debug(f"patch {p} already applied, skipping")

    def _get_working_dir(self):
        if self.__working_dir:
            return os.path.join(self.build_dir, self.__working_dir)
        else:
            return self.build_dir

    def push_location(self, path):
        self.__working_dir = path

    def pop_location(self):
        self.__working_dir = None

    def prepare_build_dir(self):
        if self.clean and os.path.exists(self.build_dir):
            shutil.rmtree(self.build_dir, onerror=_rmtree_error_handler)

        if os.path.exists(self.build_dir):
            log.debug(f"directory {self.build_dir} already exists")
            if self.update_build_dir():
                self.mark_file_remove()
                if os.path.exists(self.patch_dir):
                    log.log(f"Copying files from {self.patch_dir} to {self.build_dir}")
                    self.builder.copy_all(self.patch_dir, self.build_dir)
        else:
            self.unpack()
            if os.path.exists(self.patch_dir):
                log.log(f"Copying files from {self.patch_dir} to {self.build_dir}")
                self.builder.copy_all(self.patch_dir, self.build_dir)

    def update_build_dir(self):
        pass

    def unpack(self):
        raise NotImplementedError("unpack")

    def export(self):
        raise NotImplementedError("export")

    def get_path(self):
        # Optional for projects
        pass

    def add_extra_env(self, key, val):
        # Extra env vars for projects / tools
        self.extra_env[key] = val

    def apply_extra_env(self, base_env):
        if self.extra_env:
            for key, val in self.extra_env.items():
                if key not in base_env:
                    base_env[key] = val

    @staticmethod
    def add(proj, type=ProjectType.IGNORE):
        Project._projects.append(proj)
        Project._names.append(proj.name)
        Project._dict[proj.name] = proj
        if proj.type is None:
            proj.type = type

    @staticmethod
    def register(cls, ty):
        """Register the class to be added after some initialization."""
        Project._reg_prj_list.append(
            (
                cls,
                ty,
            )
        )

    @staticmethod
    def add_all():
        """Add all the registered class."""
        for cls, ty in Project._reg_prj_list:
            c_inst = cls()
            if c_inst.to_add:
                Project.add(c_inst, type=ty)
            else:
                del c_inst

    def ignore(self):
        """Mark the project not to build/add to the list."""
        self.to_add = False

    @staticmethod
    def get_project(name):
        try:
            return Project._dict[name]
        except KeyError:
            log.error_exit(f"Could not find project {name}")

    @staticmethod
    def list_projects():
        return list(Project._projects)

    @staticmethod
    def get_names():
        return list(Project._names)

    @staticmethod
    def get_dict():
        return dict(Project._dict)

    @staticmethod
    def get_tool_path(tool):
        if not isinstance(tool, Project):
            tool = Project._dict[tool]
        if tool.type != ProjectType.TOOL:
            return None
        t = tool.get_path()
        return t[0] or t[1] if isinstance(t, tuple) else t

    @staticmethod
    def get_tool_executable(tool):
        if not isinstance(tool, Project):
            tool = Project._dict[tool]

        return tool.get_executable() if tool.type == ProjectType.TOOL else None

    @staticmethod
    def get_tool_base_dir(tool):
        if not isinstance(tool, Project):
            tool = Project._dict[tool]

        return tool.get_base_dir() if tool.type == ProjectType.TOOL else None

    def mark_file_calc(self):
        if not self.mark_file:
            self.mark_file = os.path.join(self.build_dir, ".wingtk-built")

    def mark_file_remove(self):
        self.mark_file_calc()
        if os.path.isfile(self.mark_file):
            os.remove(self.mark_file)

    def mark_file_write(self):
        self.mark_file_calc()
        try:
            with open(self.mark_file, "w", encoding="utf-8") as fo:
                now = datetime.datetime.now().replace(microsecond=0)
                fo.write(f"{now.strftime('%Y-%m-%d %H:%M:%S')}\n")
        except FileNotFoundError as e:
            log.debug(f"Exception writing file '{self.mark_file}' ({e})")

    def mark_file_exist(self):
        rt = None
        self.mark_file_calc()
        if os.path.isfile(self.mark_file):
            try:
                with open(self.mark_file, encoding="utf-8") as fi:
                    rt = fi.readline().strip("\n")
            except OSError as e:
                print(f"Exception reading file '{self.mark_file}'")
                print(e)
        return rt

    def is_project(self):
        return self.type == ProjectType.PROJECT


def project_add(cls):
    """Class decorator to add the newly created Project class to the global
    projects/tools/groups list."""
    Project.register(cls, ProjectType.PROJECT)
    return cls


def get_project_by_type(prj_type):
    return [
        (project.name, project.version)
        for project in Project._projects
        if project.type == prj_type
    ]
