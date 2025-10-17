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
from typing import Annotated

from cyclopts import Group, Parameter, ValidationError

from gvsbuild.utils.base_project import Options, Project, ProjectType
from gvsbuild.utils.builder import Builder
from gvsbuild.utils.simple_ui import log
from gvsbuild.utils.utils import ordered_set


def validate_ninja_opts(type_, value: str) -> None:
    """Validator for ninja_opts to ensure it starts with a dash."""
    if value and not (value.startswith("-") or value.startswith("--")):
        raise ValidationError(
            f"ninja-opts must start with a dash (- or --). Got: '{value}'. "
            "Examples: --ninja-opts -j2, --ninja-opts --verbose"
        )


BUILD_CONFIG_GROUP = Group("Build Configuration", sort_key=0)
DIRECTORY_GROUP = Group("Directory Options", sort_key=1)
VS_SDK_GROUP = Group("Visual Studio and SDK Options", sort_key=2)
NET_GROUP = Group(".NET Options", sort_key=3)
BUILD_OPTIONS_GROUP = Group("Options to Pass to Build Systems", sort_key=4)
SKIP_CLEANUP_GROUP = Group("Skip and Cleanup Options", sort_key=5)
ZIP_GROUP = Group("Zip Options", sort_key=6)
INTROSPECTION_GROUP = Group("Introspection Options", sort_key=7)
OPENSSL_GROUP = Group("OpenSSL Options", sort_key=8)
FFMPEG_GROUP = Group("FFmpeg Options", sort_key=9)
LOGGING_GROUP = Group("Logging Options", sort_key=10)
ENVIRONMENT_GROUP = Group("Environment Options", sort_key=11)


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


def __parse_extra_opts(extra_opts: list[str]) -> dict[str, list[str]]:
    if extra_opts is None:
        return {}
    parsed_opts = {}
    for eo in extra_opts:
        project, opts = eo.split(":")
        parsed_opts[project] = opts.split(";")
    return parsed_opts


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


def build(
    projects: list[str],
    /,
    *,
    platform: Annotated[Platform, Parameter(group=BUILD_CONFIG_GROUP)] = Platform.x64,
    configuration: Annotated[
        Configuration, Parameter(group=BUILD_CONFIG_GROUP)
    ] = Configuration.debug_optimized,
    check_hash: Annotated[bool, Parameter(group=BUILD_CONFIG_GROUP)] = False,
    build_dir: Annotated[Path, Parameter(group=DIRECTORY_GROUP)] = Path(
        r"C:\gtk-build"
    ),
    msys_dir: Annotated[Path | None, Parameter(group=DIRECTORY_GROUP)] = None,
    archives_download_dir: Annotated[
        Path | None, Parameter(group=DIRECTORY_GROUP)
    ] = None,
    export_dir: Annotated[Path | None, Parameter(group=DIRECTORY_GROUP)] = None,
    patches_root_dir: Annotated[Path | None, Parameter(group=DIRECTORY_GROUP)] = None,
    tools_root_dir: Annotated[Path | None, Parameter(group=DIRECTORY_GROUP)] = None,
    git_expand_dir: Annotated[Path | None, Parameter(group=DIRECTORY_GROUP)] = None,
    vs_ver: Annotated[VsVer, Parameter(group=VS_SDK_GROUP)] = VsVer.vs2022,
    vs_install_path: Annotated[Path | None, Parameter(group=VS_SDK_GROUP)] = None,
    win_sdk_ver: Annotated[WinSdkVersion | None, Parameter(group=VS_SDK_GROUP)] = None,
    net_target_framework: Annotated[str | None, Parameter(group=NET_GROUP)] = None,
    net_target_framework_version: Annotated[
        str | None, Parameter(group=NET_GROUP)
    ] = None,
    msbuild_opts: Annotated[str | None, Parameter(group=BUILD_OPTIONS_GROUP)] = None,
    ninja_opts: Annotated[
        str | None,
        Parameter(
            group=BUILD_OPTIONS_GROUP,
            validator=validate_ninja_opts,
            allow_leading_hyphen=True,
        ),
    ] = None,
    cargo_opts: Annotated[str | None, Parameter(group=BUILD_OPTIONS_GROUP)] = None,
    extra_opts: Annotated[
        list[str] | None, Parameter(group=BUILD_OPTIONS_GROUP)
    ] = None,
    clean: Annotated[bool, Parameter(group=SKIP_CLEANUP_GROUP)] = False,
    clean_built: Annotated[bool, Parameter(group=SKIP_CLEANUP_GROUP)] = False,
    deps: Annotated[bool, Parameter(group=SKIP_CLEANUP_GROUP)] = True,
    skip: Annotated[list[str] | None, Parameter(group=SKIP_CLEANUP_GROUP)] = None,
    from_scratch: Annotated[bool, Parameter(group=SKIP_CLEANUP_GROUP)] = False,
    keep_tools: Annotated[bool, Parameter(group=SKIP_CLEANUP_GROUP)] = False,
    fast_build: Annotated[bool, Parameter(group=SKIP_CLEANUP_GROUP)] = False,
    keep_going: Annotated[bool, Parameter(group=SKIP_CLEANUP_GROUP)] = False,
    use_env: Annotated[bool, Parameter(group=ENVIRONMENT_GROUP)] = False,
    make_zip: Annotated[bool, Parameter(group=ZIP_GROUP)] = False,
    zip_continue: Annotated[bool, Parameter(group=ZIP_GROUP)] = False,
    py_wheel: Annotated[bool, Parameter(group=INTROSPECTION_GROUP)] = False,
    enable_gi: Annotated[bool, Parameter(group=INTROSPECTION_GROUP)] = False,
    enable_fips: Annotated[bool, Parameter(group=OPENSSL_GROUP)] = False,
    ffmpeg_enable_gpl: Annotated[bool, Parameter(group=FFMPEG_GROUP)] = False,
    log_size: Annotated[int, Parameter(group=LOGGING_GROUP)] = 0,
    log_single: Annotated[bool, Parameter(group=LOGGING_GROUP)] = False,
    capture_out: Annotated[bool, Parameter(group=LOGGING_GROUP)] = False,
    verbose: Annotated[bool, Parameter(group=LOGGING_GROUP)] = False,
    debug: Annotated[bool, Parameter(group=LOGGING_GROUP)] = False,
    print_out: Annotated[bool, Parameter(group=LOGGING_GROUP)] = False,
):
    """Build a project or a list of projects.

    Examples:
    gvsbuild build libpng libffi
        Build libpng, libffi, and their dependencies (zlib).

    gvsbuild build --no-deps glib
        Build glib only.

    gvsbuild build --skip gtk4 --skip pycairo all
        Build everything except gtk4 and pycairo

    Args:
        projects: The project to build.
        platform: The platform to build for.
        configuration: The configuration to build for. "debug-optimized" only includes debug symbols for Meson and CMake projects - other projects' build tools will interpret the option as "release".
        build_dir: The full or relative path of the directory to build in.
        msys_dir: The directory of the msys installation. If not specified, automatically searches in common locations.
        archives_download_dir: The directory to download the source archives to. It will be created. If a source archive already exists here, it won't be downloaded again. Default is the build-dir\\src.
        export_dir: The directory to export the source archives to. It will be created. It creates an archive with the source code and any possible patch. Default is the build-dir\\export.
        patches_root_dir: The directory where you checked out https://github.com/wingtk/gvsbuild.git. Default is the build-dir\\github\\gvsbuild.
        tools_root_dir: The directory where to install the downloaded tools. Default is $(build-dir)\\tools.
        vs_ver: Visual Studio version 12 (vs2013), 14 (vs2015), 15 (vs2017), 16 (vs2019), 17 (vs2022).
        vs_install_path: The directory where you installed Visual Studio. Default is 'C:\\Program Files (x86)\\Microsoft Visual Studio $(vs-ver).0' (for vs-ver <= 14) or 'C:\\Program Files (x86)\\Microsoft Visual Studio\\20xx (2017 for vs-ver 15, 2019 for vs-ver 16, ...). If not set, the script look automatically under Professional, BuildTools, Enterprise, Community, and Preview sub directory until it finds the startup batch file.
        win_sdk_ver: The Windows SDK version to use for building, used to initialize the Visual Studio build environment. It can be 8.1 (for windows 8 compatibility) or 10.0.xxxxx.0, where xxxxx, at the moment, can be 10150, 10240, 10586, 14393, 15063, 16299, 17134, or 17763 depending on the VS version / installation's options. If you don't specify one the scripts tries to locate the used one to pass the value to the msbuild command.
        net_target_framework: .net target framework. If set then TargetFrameworks parameter is passed down to msbuild with the specific target. i.e net45.
        net_target_framework_version: .net target framework version. If set then TargetFrameworkVersion parameter is passed down to msbuild with the specific version. i.e v4.6.2.
        check_hash: If set, only check the hash of the downloaded archives, no build.
        clean: If set, clean the build directory before building.
        clean_built: If set, clean only the projects asked on the command line, not all the ones to build (via a dependency).
        deps: If not set, don't build the dependencies of the projects.
        msbuild_opts: Command line options to pass to msbuild.
        skip: Project to avoid building, can be run multiple times.
        use_env: Use and keep the calling environment for LIB, LIBPATH, INCLUDE and PATH.
        make_zip: Create singles zips of the projects built under the build-dir\\dist\\vsXXXX[-sdkVer]\\[platform]\\[configuration], for example 'C:\\gtk-build\\dist\\vs2015-8.1\\win32\\release'. NOTE: the destination dir (e.g. 'C:\\gtk-build\\gtk\\win32\\release') will be cleared completely before the build!
        zip_continue: If set, don't initialize the zip creation phase and keep the destination dir.
        from_scratch: Start from scratch, deleting the build and the destination directories of the project for the current platform/configuration setup (e.g. 'C:\\gtk-build\\build\\x64\\release' and 'C:\\gtk-build\\gtk\\x64\\release' and the common tools ('C:\\gtk-build\\tools').
        keep_tools: Active only when used with --from-scratch, keep and don't delete the (common) tool directory.
        fast_build: Don't build a project if it's already built and not updated. Note: you can have wrong results if you change only the patches or the script (updating the tarball or the git source is handled correctly).
        keep_going: Continue the build even on errors, dropping the projects that depends on the failed ones.
        py_wheel: pycairo/pygobject: build also the wheel distribution format.
        enable_gi: For the GTK stack, create the .gir/.typelib files for gobject introspection.
        enable_fips: Build the FIPS validated cryptographic module.
        ffmpeg_enable_gpl: ffmpeg: build with the gpl libraries/modules.
        log_size: Maximum log size (in kilobytes) before restarting with a new file.
        log_single: If set, always start a new log file, with date and time.
        capture_out: If set, capture the output of the build commands and write it to the log file.
        verbose: If set, print the output of the build commands to the console.
        debug: If set, print debug messages to the console.
        print_out: With --capture-out active print the result of the commands also on stdout.
        ninja_opts: Command line options to pass to ninja, e.g. to limit the use (-j 2) or for debug purposes.
        cargo_opts: Command line options to pass to cargo.
        extra_opts: Additional command line options to pass to specific project. Example: --extra_opts <project>:<option1>[;<option1>...].
        git_expand_dir: The directory where the projects from git are expanded and updated.
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
    opts.extra_opts = __parse_extra_opts(extra_opts if extra_opts else [])
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
