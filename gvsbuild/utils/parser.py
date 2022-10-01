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

"""Command line parser."""

import argparse
import os
import re
import sys
from pathlib import Path
from typing import Any, Tuple, Union

from .base_project import Options, Project, ProjectType
from .builder import Builder
from .simple_ui import log
from .utils import ordered_set


def get_options(args):
    opts = Options()

    opts.verbose = args.verbose
    opts.debug = args.debug
    opts.platform = args.platform
    opts.configuration = getattr(args, "configuration", "release")
    opts.build_dir = args.build_dir
    opts.archives_download_dir = args.archives_download_dir
    opts.export_dir = args.export_dir
    opts.patches_root_dir = args.patches_root_dir
    opts.tools_root_dir = args.tools_root_dir
    opts.vs_ver = args.vs_ver
    opts.vs_install_path = args.vs_install_path
    opts.win_sdk_ver = args.win_sdk_ver
    opts.net_target_framework = args.net_target_framework
    opts.net_target_framework_version = args.net_target_framework_version
    opts.python_dir = args.python_dir
    opts.msys_dir = args.msys_dir
    opts.clean = args.clean
    opts.msbuild_opts = args.msbuild_opts
    opts.use_env = args.use_env
    opts.no_deps = args.no_deps
    opts.check_hash = args.check_hash
    opts.skip = args.skip
    opts.make_zip = args.make_zip
    opts.zip_continue = args.zip_continue
    opts.from_scratch = args.from_scratch
    opts.keep_tools = args.keep_tools
    opts.fast_build = args.fast_build
    opts.keep = args.keep
    opts.clean_built = args.clean_built
    opts.py_wheel = args.py_wheel
    opts.enable_gi = args.enable_gi
    opts.ffmpeg_enable_gpl = args.ffmpeg_enable_gpl
    opts.log_size = args.log_size
    opts.log_single = args.log_single
    opts.cargo_opts = args.cargo_opts
    opts.ninja_opts = args.ninja_opts
    opts.python_ver = args.python_ver
    opts.same_python = args.same_python
    opts.capture_out = args.capture_out
    opts.print_out = args.print_out
    opts.git_expand_dir = args.git_expand_dir

    # active the log
    log.configure(os.path.join(opts.build_dir, "logs"), opts)

    if opts.make_zip and opts.no_deps:
        log.error_exit("Options --make-zip and --no-deps are not compatible")

    if not opts.archives_download_dir:
        opts.archives_download_dir = os.path.join(args.build_dir, "src")
    if not opts.git_expand_dir:
        opts.git_expand_dir = os.path.join(opts.archives_download_dir, "git-exp")
    if not opts.export_dir:
        opts.export_dir = os.path.join(args.build_dir, "export")
    if not opts.patches_root_dir:
        opts.patches_root_dir = str(Path(__file__).parent.parent / "patches")
    prop_file = os.path.join(opts.patches_root_dir, "stack.props")
    if not os.path.isfile(prop_file):
        log.error_exit(
            "Missing 'stack.props' file on directory '%s'.\nWrong or missing --patches-root-dir option?"
            % (opts.patches_root_dir,)
        )

    if not opts.tools_root_dir:
        opts.tools_root_dir = os.path.join(args.build_dir, "tools")

    if opts.python_dir is None and not opts.same_python:
        opts._load_python = True

    opts.projects = args.project
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

    return opts


def __get_projects_to_build(opts):
    to_build = ordered_set()
    if opts._load_python:
        # We use nuget to download & install the python needed for the build so we put it at the beginning
        opts.projects.insert(0, "python")

    for name in opts.projects:
        p = Project.get_project(name)
        if not opts.no_deps:
            for dep in p.all_dependencies:
                to_build.add(dep)
        to_build.add(p)
        if opts.clean_built:
            p.clean = True

    # See if we need to drop some project
    if opts.skip:
        to_skip = opts.skip.split(",")
        for s in to_skip:
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


def do_build(args):
    opts = get_options(args)
    if log.debug_on():
        log.debug("Options are:")
        for co in sorted(opts.__dict__.keys()):
            v = opts.__dict__[co]
            pv = f"'{v}'" if type(v) is str else repr(v)
            log.message_indent(f"'{co}': {pv}, ")
    builder = Builder(opts)
    builder.preprocess()

    to_build = __get_projects_to_build(opts)
    if not to_build:
        log.error_exit("nothing to do")
    log.debug(f"building {[p.name for p in to_build]}")

    builder.build(to_build)


def get_project_by_type(prj_type):
    return [
        (project.name, project.version)
        for project in Project._projects
        if project.type == prj_type
    ]


def do_list(args):
    def do_list_type(prj_type, desc):
        projects = get_project_by_type(prj_type)
        if projects:
            projects.sort()

            print(f"{desc}:")
            for project in projects:
                print(f"\t{project[0]:<{Project.name_len}} {project[1]}")

    # now add the tools/projects/groups
    Project.add_all()
    do_list_type(ProjectType.TOOL, "Available tools")
    do_list_type(ProjectType.PROJECT, "Available projects")
    do_list_type(ProjectType.GROUP, "Available groups")
    do_list_type(ProjectType.IGNORE, "Developer project(s)")
    sys.exit(0)


def separate_name_and_major_version(name: str) -> Tuple[Union[str, Any], ...]:
    # Exceptions where ending with a simple digit is part of the library name
    if name in {"nghttp2", "ssh2", "libxml2", "libtiff-4"}:
        return name, None
    # https://regex101.com/r/1c4iLx/2
    match = re.search(r"([a-z-]*\d{3}|[a-z-]*\d{0})(\d$)?", name)
    return match.group(1, 2) if match else (None, None)


def do_outdated(args):
    try:
        import lastversion
        from packaging import version
    except ImportError:
        print("Please pip install .[outdated] in your Python environment")
        sys.exit(0)

    Project.add_all()
    projects = get_project_by_type(ProjectType.PROJECT)
    projects.extend(get_project_by_type(ProjectType.TOOL))
    print("Looking for projects and tools that are out-of-date, please submit a PR!")
    print(f"\t{'Project Name':<{Project.name_len}} {'Current':<45} {'Latest':<45}")
    try:
        for project in projects:
            # glib-py-wrapper and check-libs are vendored in gvsbuild
            if project[0] in ("glib-py-wrapper", "check-libs") or not project[1]:
                continue
            name_and_major = separate_name_and_major_version(project[0])
            repos = {
                "adwaita-icon-theme": "https://gitlab.gnome.org/GNOME/adwaita-icon-theme",
                "atk": "https://gitlab.gnome.org/GNOME/atk",
                "boringssl": "https://github.com/google/boringssl",
                "clutter": "https://gitlab.gnome.org/GNOME/clutter",
                "cogl": "https://gitlab.gnome.org/Archive/cogl",
                "emeus": "https://github.com/ebassi/emeus",
                "fontconfig": "https://gitlab.freedesktop.org/fontconfig/fontconfig",
                "freetype": "https://gitlab.freedesktop.org/freetype/freetype",
                "gdk-pixbuf": "https://gitlab.gnome.org/GNOME/gdk-pixbuf",
                "gettext": "autotools-mirror/gettext",
                "glib": "https://gitlab.gnome.org/GNOME/glib",
                "glib-networking": "https://gitlab.gnome.org/GNOME/glib-networking",
                "glib-py-wrapper": "https://gitlab.gnome.org/GNOME/glib-py-wrapper",
                "gobject-introspection": "https://gitlab.gnome.org/GNOME/gobject-introspection",
                "graphene": "ebassi/graphene",
                "gsettings-desktop-schemas": "https://gitlab.gnome.org/GNOME/gsettings-desktop-schemas",
                "gtk3": "https://gitlab.gnome.org/GNOME/gtk",
                "gtk4": "https://gitlab.gnome.org/GNOME/gtk",
                "gtksourceview4": "https://gitlab.gnome.org/GNOME/gtksourceview",
                "gtksourceview5": "https://gitlab.gnome.org/GNOME/gtksourceview",
                "hicolor-icon-theme": "https://gitlab.freedesktop.org/xdg/default-icon-theme",
                "json-glib": "https://gitlab.gnome.org/GNOME/json-glib",
                "libcroco": "https://gitlab.gnome.org/Archive/libcroco",
                "libcurl": "https://github.com/curl/curl",
                "libmicrohttpd": "https://github.com/Karlson2k/libmicrohttpd",
                "libsoup2": "https://gitlab.gnome.org/GNOME/libsoup",
                "libsoup3": "https://gitlab.gnome.org/GNOME/libsoup",
                "libssh": "libssh/libssh-mirror",
                "libssh2": "libssh2/libssh2",
                "libtiff-4": "https://gitlab.com/libtiff/libtiff",
                "libxml2": "https://gitlab.gnome.org/GNOME/libxml2",
                "orc": "https://gitlab.freedesktop.org/gstreamer/orc",
                "pango": "https://gitlab.gnome.org/GNOME/pango",
                "pixman": "https://gitlab.freedesktop.org/pixman/pixman",
                "pkg-config": "pkgconf",
                "pygobject": "https://gitlab.gnome.org/GNOME/pygobject",
                "wing": "https://gitlab.gnome.org/GNOME/wing",
            }
            try:
                repo = repos.get(project[0], name_and_major[0])
                if name_and_major[1]:
                    latest_version = lastversion.latest(
                        repo=repo, major=name_and_major[1]
                    )
                else:
                    latest_version = lastversion.latest(
                        repo=repo,
                    )
                if not latest_version:
                    print(
                        f"\t{project[0]:<{Project.name_len}} {project[1]:<45} {'No release found':<45}"
                    )
                elif version.parse(str(latest_version)) > version.parse(project[1]):
                    print(
                        f"\t{project[0]:<{Project.name_len}} {project[1]:<45} {str(latest_version):<45}"
                    )
            except version.InvalidVersion:
                print(f"Project {project[0]} does not have a valid version")
    except lastversion.utils.ApiCredentialsError:
        print("Set GITHUB_API_TOKEN=xxxxxxxxxxxxxxx environmental variable")


def create_parser():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="Jhbuild-like system for Windows to build Gtk and friends",
        fromfile_prefix_chars="@",
        epilog="""
Examples:
    gvsbuild build libpng libffi
        Build libpng, libffi, and their dependencies (zlib).

    gvsbuild build --no-deps glib
        Build glib only.

    gvsbuild build --skip gtk3,pycairo,pygobject all
        Build everything except gtk3, pycairo, and pygobject
    """,
    )

    # ==============================================================================
    # Global options
    # ==============================================================================

    parser.add_argument(
        "-v",
        "--verbose",
        default=False,
        action="store_true",
        help="Print lots of stuff.",
    )
    parser.add_argument(
        "-d",
        "--debug",
        default=False,
        action="store_true",
        help="Print even more stuff.",
    )

    subparsers = parser.add_subparsers()

    # ==============================================================================
    # build
    # ==============================================================================

    p_build = subparsers.add_parser("build", help="build project(s)")
    p_build.set_defaults(func=do_build)

    p_build.add_argument(
        "-p",
        "--platform",
        default="x64",
        choices=["x86", "x64"],
        help="Platform to build for, x86 or x64. Default is x64.",
    )
    p_build.add_argument(
        "-c",
        "--configuration",
        default="release",
        choices=["release", "debug"],
        help="Configuration to build, release or debug. Default is release.",
    )
    p_build.add_argument(
        "--build-dir",
        default=r"C:\gtk-build",
        help="The directory where the sources will be downloaded and built.",
    )
    p_build.add_argument(
        "--msys-dir",
        default=r"C:\Msys64",
        help="The directory where you installed msys2.",
    )
    p_build.add_argument(
        "--archives-download-dir",
        help="The directory to download the source archives to. It will be created. "
        + "If a source archive already exists here, it won't be downloaded again. "
        + "Default is $(build-dir)\\src.",
    )
    p_build.add_argument(
        "--export-dir",
        help="The directory to export the source archives to. It will be created. "
        + "It creates an archive with the source code and any possible patch. "
        + "Default is $(build-dir)\\export.",
    )
    p_build.add_argument(
        "--patches-root-dir",
        help="The directory where you checked out https://github.com/wingtk/gvsbuild.git. Default is $(build-dir)\\github\\gvsbuild.",
    )
    p_build.add_argument(
        "--tools-root-dir",
        help="The directory where to install the downloaded tools. Default is $(build-dir)\\tools.",
    )
    p_build.add_argument(
        "--vs-ver",
        default="17",
        help="Visual Studio version 12 (vs2013), 14 (vs2015), 15 (vs2017), 16 (vs2019), 17 (vs2022). Default is 17.",
    )
    p_build.add_argument(
        "--vs-install-path",
        help=r"The directory where you installed Visual Studio. Default is 'C:\Program Files (x86)\Microsoft Visual Studio $(vs-ver).0' (for vs-ver <= 14) "
        + "or 'C:\\Program Files (x86)\\Microsoft Visual Studio\\20xx' (2017 for vs-ver 15, 2019 for vs-ver 16, ...). "
        "If not set for the vs2017 version the script look automatically under Professional, BuildTools, Enterprise, Community and Preview sub directory until it finds the startup batch.",
    )
    p_build.add_argument(
        "--win-sdk-ver",
        default=None,
        help=r"The windows sdk version to use for building, used to initialize the Visual Studio build environment. "
        + "It can be 8.1 (for windows 8 compatibility) or 10.0.xxxxx.0, where xxxxx, at the moment, can be 10150, 10240, 10586, 14393, 15063 "
        + "16299, 17134 or 17763 "
        + "depending on the VS version / installation's options. "
        + "If you don't specify one the scripts tries to locate the used one to pass the value to the msbuild command.",
    )
    p_build.add_argument(
        "--net-target-framework",
        default=None,
        help=".net target framework. If set then TargetFrameworks parameter is passed down to msbuild with the specific target. i.e net45",
    )
    p_build.add_argument(
        "--net-target-framework-version",
        default=None,
        help=".net target framework version. If set then TargetFrameworkVersion parameter is passed down to msbuild with the specific version. i.e v4.6.2",
    )
    p_build.add_argument(
        "--python-ver",
        default="3.10",
        help="Python version to download and use for the build (3.10, 3.9, 3.8, 3.7, or the exact one, 3.10.2 or 3.8.0-a3.",
    )
    p_build.add_argument(
        "--python-dir",
        default=None,
        help="The directory containing the python you want to use for the build of the projects (not the one used to run the script).",
    )
    p_build.add_argument(
        "--same-python",
        default=False,
        action="store_true",
        help="Use for the build the same python used to run this script",
    )

    p_build.add_argument(
        "--check-hash",
        default=False,
        action="store_true",
        help="Only check hashes of downloaded archive(s), no build",
    )
    p_build.add_argument(
        "--clean",
        default=False,
        action="store_true",
        help="Build the project(s) from scratch",
    )
    p_build.add_argument(
        "--clean-built",
        default=False,
        action="store_true",
        help="Clean before the build only the project(s) asked on the command line, not all the ones to build (via a dependency)",
    )
    p_build.add_argument(
        "--no-deps",
        default=False,
        action="store_true",
        help="Do not build dependencies of the selected project(s)",
    )

    p_build.add_argument(
        "--msbuild-opts", default="", help="Command line options to pass to msbuild."
    )
    p_build.add_argument(
        "--use-env",
        default=False,
        action="store_true",
        help="Use and keep the calling environment for LIB, LIBPATH, INCLUDE and PATH",
    )

    p_build.add_argument(
        "--skip",
        default="",
        help="A comma separated list of project(s) not to build. For dev-shell is a list of tool not to activate.",
    )

    p_build.add_argument(
        "--make-zip",
        default=False,
        action="store_true",
        help="Create singles zips of the projects built under $(build-dir)\\dist\\vsXXXX[-sdkVer]\\[platform]\\[configuration], "
        + "for example 'c:\\gtk-build\\dist\\vs2015-8.1\\win32\\release'. "
        + "NOTE: the destination dir (e.g. 'c:\\gtk-build\\gtk\\win32\\release') "
        + "will be cleared completely before the build!",
    )
    p_build.add_argument(
        "--zip-continue",
        default=False,
        action="store_true",
        help="Don't initialize the zip creation phase and keep the destination dir.",
    )
    p_build.add_argument(
        "--from-scratch",
        default=False,
        action="store_true",
        help="Start from scratch, deleting, before starting the build, the build and the "
        + "destination directories of the project for the current platform/configuration "
        + "setup (e.g. 'c:\\gtk-build\\build\\win32\\release' and 'c:\\gtk-build\\gtk\\win32\\release'  "
        + "and the common tools ('c:\\gtk-build\\tools')",
    )
    p_build.add_argument(
        "--keep-tools",
        default=False,
        action="store_true",
        help="Active only when used with --from-scratch, keep and don't delete the (common) tool directory.",
    )
    p_build.add_argument(
        "--fast-build",
        default=False,
        action="store_true",
        help="Don't build a project if it's already built and not updated."
        + "Note: you can have wrong results if you change only the patches or the script (updating the tarball or the git source is handled correctly)",
    )
    p_build.add_argument(
        "-k",
        "--keep",
        default=False,
        action="store_true",
        help="Continue the build even on errors, dropping the projects that depends on the failed ones",
    )
    p_build.add_argument(
        "--py-wheel",
        default=False,
        action="store_true",
        help="pycairo/pygobject: build also the wheel distribution format",
    )
    p_build.add_argument(
        "--enable-gi",
        default=False,
        action="store_true",
        help="Create, for the gtk stack, the .gir/.typelib files for gobject introspection",
    )
    p_build.add_argument(
        "--ffmpeg-enable-gpl",
        default=False,
        action="store_true",
        help="ffmpeg: build with the gpl libraries/modules",
    )
    p_build.add_argument(
        "--log-size",
        default=0,
        type=int,
        help="Maximum log size (in kilobytes) before restarting with a new file",
    )
    p_build.add_argument(
        "--log-single",
        default=False,
        action="store_true",
        help="Always start a new log file, with date & time",
    )
    p_build.add_argument(
        "--capture-out",
        default=False,
        action="store_true",
        help="Capture the output of the build process and put it in the log file.",
    )
    p_build.add_argument(
        "--print-out",
        default=False,
        action="store_true",
        help="With --capture-out acrive print the result of the commands also on stdout.",
    )
    p_build.add_argument(
        "--ninja-opts",
        default="",
        help="Command line options to pass to ninja, e.g. to limit the use (-j 2) or for debug purpouse.",
    )
    p_build.add_argument(
        "--cargo-opts", default="", help="Command line options to pass to cargo."
    )
    p_build.add_argument(
        "--git-expand-dir",
        default=None,
        help="The directory where the projects from git are expanded and updated.",
    )
    p_build.add_argument("project", nargs="+", help="Project(s) to build.")

    # ==============================================================================
    # list
    # ==============================================================================

    p_list = subparsers.add_parser("list", help="list available projects")
    p_list.set_defaults(func=do_list)

    # ==============================================================================
    # outdated
    # ==============================================================================

    p_outdated = subparsers.add_parser(
        "outdated", help="list out of date projects and tools"
    )
    p_outdated.set_defaults(func=do_outdated)

    return parser
