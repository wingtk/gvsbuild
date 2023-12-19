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

from enum import Enum
from pathlib import Path
from typing import List

import typer

from gvsbuild.utils.base_project import Options, Project, ProjectType
from gvsbuild.utils.builder import Builder
from gvsbuild.utils.simple_ui import log
from gvsbuild.utils.utils import ordered_set


def __get_projects_to_build(opts):
    to_build = ordered_set()
    for name in opts.projects:
        if name == "all":
            for proj in Project.list_projects():
                if proj.type == ProjectType.PROJECT:
                    to_build.add(proj)
        p = Project.get_project(name)
        if opts.deps:
            for dep in p.all_dependencies:
                to_build.add(dep)
        to_build.add(p)
        if opts.clean_built:
            p.clean = True
        if name == "openssl" and opts.enable_fips:
            to_build.add(Project.get_project("openssl-fips"))

    # See if we need to drop some project
    if opts.skip:
        for s in opts.skip:
            if s not in Project.get_names():
                log.error_exit(
                    s
                    + " is not a valid project name, available projects are:\n\t"
                    + "\n\t".join(Project.get_names())
                )

            p = Project.get_project(s)
            if p in to_build:
                log.debug(f"Dropped project {s}")
                to_build.remove(p)
    return to_build


class Platform(str, Enum):
    x64 = "x64"
    x86 = "x86"


class Configuration(str, Enum):
    debug = "debug"
    release = "release"
    debug_optimized = "debug-optimized"


class VsVer(str, Enum):
    vs2013 = "12"
    vs2015 = "14"
    vs2017 = "15"
    vs2019 = "16"
    vs2022 = "17"


class WinSdkVersion(str, Enum):
    sdk_8 = "8.1"
    sdk_10150 = "10.0.10150.0"
    sdk_10240 = "10.0.10240.0"
    sdk_10586 = "10.0.10586.0"
    sdk_14393 = "10.0.14393.0"
    sdk_15063 = "10.0.15063.0"
    sdk_16299 = "10.0.16299.0"
    sdk_17134 = "10.0.17134.0"
    sdk_17763 = "10.0.17763.0"
    sdk_22621 = "10.0.22621.0"


class PythonVersion(str, Enum):
    py37 = "3.7"
    py38 = "3.8"
    py39 = "3.9"
    py310 = "3.10"


def build(
    projects: List[str] = typer.Argument(..., help="The project to build"),
    platform: Platform = typer.Option(Platform.x64, help="The platform to build for"),
    configuration: Configuration = typer.Option(
        Configuration.debug_optimized,
        help='The configuration to build for. "debug-optimized" only '
        "includes debug symbols for Meson and CMake projects - other "
        'projects\' build tools will interpret the option as "release"',
    ),
    build_dir: Path = typer.Option(
        Path(r"C:\gtk-build"),
        help="The full or relative path of the directory to build in",
        rich_help_panel="Directory Options",
    ),
    msys_dir: Path = typer.Option(
        None,
        help="The directory of the msys installation. If not specified, automatically searches in common locations",
        rich_help_panel="Directory Options",
        exists=True,
        dir_okay=True,
        resolve_path=True,
    ),
    archives_download_dir: Path = typer.Option(
        None,
        help="The directory to download the source archives to. It will be created. "
        "If a source archive already exists here, it won't be downloaded again. "
        "Default is the build-dir\\src.",
        rich_help_panel="Directory Options",
    ),
    export_dir: Path = typer.Option(
        None,
        help="The directory to export the source archives to. It will be created. "
        "It creates an archive with the source code and any possible patch. "
        "Default is the build-dir\\export.",
        rich_help_panel="Directory Options",
    ),
    patches_root_dir: Path = typer.Option(
        None,
        help="The directory where you checked out https://github.com/wingtk/gvsbuild.git. Default is the build-dir\\github\\gvsbuild.",
        rich_help_panel="Directory Options",
    ),
    tools_root_dir: Path = typer.Option(
        None,
        help="The directory where to install the downloaded tools. Default is $(build-dir)\\tools.",
        rich_help_panel="Directory Options",
    ),
    vs_ver: VsVer = typer.Option(
        VsVer.vs2022,
        help="Visual Studio version 12 (vs2013), 14 (vs2015), 15 (vs2017), 16 (vs2019), 17 (vs2022)",
        rich_help_panel="Visual Studio and SDK Options",
    ),
    vs_install_path: Path = typer.Option(
        None,
        help=r"The directory where you installed Visual Studio."
        r"Default is 'C:\Program Files (x86)\Microsoft Visual Studio $(vs-ver).0' (for vs-ver <= 14) "
        r"or 'C:\Program Files (x86)\Microsoft Visual Studio\20xx (2017 for vs-ver 15, 2019 for vs-ver 16, "
        r"...). If not set, the script look automatically under Professional, BuildTools, "
        r"Enterprise, Community, and Preview sub directory until it finds the startup batch file.",
        rich_help_panel="Visual Studio and SDK Options",
    ),
    win_sdk_ver: WinSdkVersion = typer.Option(
        None,
        help=r"The Windows SDK version to use for building, used to initialize the Visual Studio build environment. "
        "It can be 8.1 (for windows 8 compatibility) or 10.0.xxxxx.0, where xxxxx, at the moment, can be 10150, 10240, "
        "10586, 14393, 15063, 16299, 17134, or 17763 depending on the VS version / installation's options. "
        "If you don't specify one the scripts tries to locate the used one to pass the value to the msbuild command.",
        rich_help_panel="Visual Studio and SDK Options",
    ),
    net_target_framework: str = typer.Option(
        None,
        help=".net target framework. If set then TargetFrameworks parameter is passed down to msbuild with the "
        "specific target. i.e net45",
        rich_help_panel=".NET Options",
    ),
    net_target_framework_version: str = typer.Option(
        None,
        help=".net target framework version. If set then TargetFrameworkVersion parameter is passed down to "
        "msbuild with the specific version. i.e v4.6.2",
        rich_help_panel=".NET Options",
    ),
    check_hash: bool = typer.Option(
        False,
        help="If set, only check the hash of the downloaded archives, no build.",
    ),
    clean: bool = typer.Option(
        False,
        help="If set, clean the build directory before building.",
        rich_help_panel="Skip and Cleanup Options",
    ),
    clean_built: bool = typer.Option(
        False,
        help="If set, clean only the projects asked on the command line, not all the ones to build (via a dependency)",
        rich_help_panel="Skip and Cleanup Options",
    ),
    deps: bool = typer.Option(
        True,
        help="If not set, don't build the dependencies of the projects.",
        rich_help_panel="Skip and Cleanup Options",
    ),
    msbuild_opts: str = typer.Option(
        None,
        help="Command line options to pass to msbuild.",
        rich_help_panel="Options to Pass to Build Systems",
    ),
    skip: List[str] = typer.Option(
        None,
        help="Project to avoid building, can be run multiple times.",
        rich_help_panel="Skip and Cleanup Options",
    ),
    use_env: bool = typer.Option(
        False,
        help="Use and keep the calling environment for LIB, LIBPATH, INCLUDE and PATH",
        rich_help_panel="Environment Options",
    ),
    make_zip: bool = typer.Option(
        False,
        help="Create singles zips of the projects built under the build-dir\\dist\\vsXXXX[-sdkVer]\\[platform]\\[configuration], "
        "for example 'C:\\gtk-build\\dist\\vs2015-8.1\\win32\\release'. "
        "NOTE: the destination dir (e.g. 'C:\\gtk-build\\gtk\\win32\\release') "
        "will be cleared completely before the build!",
        rich_help_panel="Zip Options",
    ),
    zip_continue: bool = typer.Option(
        False,
        help="If set, don't initialize the zip creation phase and keep the destination dir.",
        rich_help_panel="Zip Options",
    ),
    from_scratch: bool = typer.Option(
        False,
        help="Start from scratch, deleting the build and the "
        "destination directories of the project for the current "
        "platform/configuration "
        "setup (e.g. 'C:\\gtk-build\\build\\x64\\release' and "
        "'C:\\gtk-build\\gtk\\x64\\release' and the common tools ('C:\\gtk-build\\tools')",
        rich_help_panel="Skip and Cleanup Options",
    ),
    keep_tools: bool = typer.Option(
        False,
        help="Active only when used with --from-scratch, keep and don't delete the (common) tool directory.",
        rich_help_panel="Skip and Cleanup Options",
    ),
    fast_build: bool = typer.Option(
        False,
        help="Don't build a project if it's already built and not updated."
        "Note: you can have wrong results if you change only the patches or the script (updating the tarball or "
        "the git source is handled correctly)",
        rich_help_panel="Skip and Cleanup Options",
    ),
    keep_going: bool = typer.Option(
        False,
        help="Continue the build even on errors, dropping the projects that depends on the failed ones",
        rich_help_panel="Skip and Cleanup Options",
    ),
    py_wheel: bool = typer.Option(
        False,
        help="pycairo/pygobject: build also the wheel distribution format",
        rich_help_panel="Introspection Options",
    ),
    enable_gi: bool = typer.Option(
        False,
        help="For the GTK stack, create the .gir/.typelib files for gobject introspection",
        rich_help_panel="Introspection Options",
    ),
    enable_fips: bool = typer.Option(
        False,
        help="Build the FIPS validated cryptographic module",
        rich_help_panel="OpenSSL Options",
    ),
    ffmpeg_enable_gpl: bool = typer.Option(
        False,
        help="ffmpeg: build with the gpl libraries/modules",
        rich_help_panel="FFmpeg Options",
    ),
    log_size: int = typer.Option(
        0,
        help="Maximum log size (in kilobytes) before restarting with a new file",
        rich_help_panel="Logging Options",
    ),
    log_single: bool = typer.Option(
        False,
        help="If set, always start a new log file, with date and time",
        rich_help_panel="Logging Options",
    ),
    capture_out: bool = typer.Option(
        False,
        help="If set, capture the output of the build commands and write it to the log file",
        rich_help_panel="Logging Options",
    ),
    verbose: bool = typer.Option(
        False,
        help="If set, print the output of the build commands to the console",
        rich_help_panel="Logging Options",
    ),
    debug: bool = typer.Option(
        False,
        help="If set, print debug messages to the console",
        rich_help_panel="Logging Options",
    ),
    print_out: bool = typer.Option(
        False,
        help="With --capture-out active print the result of the commands also on stdout.",
        rich_help_panel="Logging Options",
    ),
    ninja_opts: str = typer.Option(
        None,
        help="Command line options to pass to ninja, e.g. to limit the use (-j 2) or for debug purposes.",
        rich_help_panel="Options to Pass to Build Systems",
    ),
    cargo_opts: str = typer.Option(
        None,
        help="Command line options to pass to cargo",
        rich_help_panel="Options to Pass to Build Systems",
    ),
    git_expand_dir: Path = typer.Option(
        None,
        help="The directory where the projects from git are expanded and updated.",
        rich_help_panel="Directory Options",
    ),
):
    """Build a project or a list of projects.

    gvsbuild build libpng libffi
        Build libpng, libffi, and their dependencies (zlib).

    gvsbuild build --no-deps glib
        Build glib only.

    gvsbuild build --skip gtk4 --skip pycairo all
        Build everything except gtk4 and pycairo
    """
    opts = Options()
    opts.verbose = verbose
    opts.debug = debug
    if build_dir:
        build_dir = Path(build_dir).resolve()
    opts.build_dir = str(build_dir)
    log.configure(str(build_dir / "logs"), opts)
    opts.platform = platform.value
    opts.configuration = configuration.value
    if opts.configuration == Configuration.debug_optimized:
        # Some build systems take "opts.configuration" directly, and won't support our
        # custom "debug-optimized" string. Convert it back to the standard
        # "release" string but track that we still want debug symbols where possible.
        opts.configuration = Configuration.release.value
        opts.release_configuration_is_actually_debug_optimized = True
    log.message(f"Build type is {configuration}")
    if not archives_download_dir:
        archives_download_dir = build_dir / "src"
    opts.archives_download_dir = str(archives_download_dir)
    opts.export_dir = str(export_dir) if export_dir else str(build_dir / "export")
    if not patches_root_dir:
        patches_root_dir = Path(__file__).parent / "patches"
    opts.patches_root_dir = str(patches_root_dir)
    if tools_root_dir:
        opts.tools_root_dir = str(tools_root_dir)
    else:
        opts.tools_root_dir = str(build_dir / "tools")
    opts.vs_ver = vs_ver.value
    opts.vs_install_path = vs_install_path
    opts.win_sdk_ver = win_sdk_ver.value if win_sdk_ver else None
    if git_expand_dir:
        opts.git_expand_dir = str(git_expand_dir)
    else:
        opts.git_expand_dir = str(archives_download_dir / "git-exp")
    opts.net_target_framework = net_target_framework
    opts.net_target_framework_version = net_target_framework_version
    opts.msys_dir = msys_dir
    opts.clean = clean
    opts.msbuild_opts = msbuild_opts
    opts.use_env = use_env
    opts.deps = deps
    opts.check_hash = check_hash
    opts.skip = skip
    opts.make_zip = make_zip
    opts.zip_continue = zip_continue
    opts.from_scratch = from_scratch
    opts.keep_tools = keep_tools
    opts.fast_build = fast_build
    opts.keep_going = keep_going
    opts.clean_built = clean_built
    opts.py_wheel = py_wheel
    opts.enable_gi = enable_gi
    opts.enable_fips = enable_fips
    opts.ffmpeg_enable_gpl = ffmpeg_enable_gpl
    opts.log_size = log_size
    opts.log_single = log_single
    opts.cargo_opts = cargo_opts
    opts.ninja_opts = ninja_opts
    opts.capture_out = capture_out
    opts.print_out = print_out

    if opts.make_zip and not opts.deps:
        log.error_exit("Options --make-zip and --no-deps are not compatible")
    prop_file = patches_root_dir / "stack.props"
    if not Path.is_file(prop_file):
        log.error_exit(
            f"Missing 'stack.props' file on directory {opts.patches_root_dir}.\n"
            "Wrong or missing --patches-root-dir option?"
        )

    opts.projects = projects
    Project.opts = opts
    # now add the tools/projects/groups
    Project.add_all()

    for p in opts.projects:
        if p not in Project.get_names():
            log.error_exit(
                p
                + " is not a valid project name, available projects are:\n\t"
                + "\n\t".join(Project.get_names())
            )

    if log.debug_on():
        log.debug("Options are:")
        for co in sorted(opts.__dict__.keys()):
            v = opts.__dict__[co]
            pv = f"'{v}'" if isinstance(v, str) else repr(v)
            log.message_indent(f"'{co}': {pv}, ")
    builder = Builder(opts)
    builder.preprocess()

    to_build = __get_projects_to_build(opts)
    if not to_build:
        log.error_exit("nothing to do")
    log.debug(f"building {[p.name for p in to_build]}")

    builder.build(to_build)
