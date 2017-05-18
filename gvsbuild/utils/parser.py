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

"""
Command line parser
"""

import argparse
import os
import sys

from .base_project import Project, GVSBUILD_PROJECT, GVSBUILD_TOOL, GVSBUILD_GROUP
from .builder import Builder
from .utils import ordered_set
from .simple_ui import error_exit, print_debug

class Options(object):
    pass

def get_options(args):
    opts = Options()

    opts.platform = args.platform
    opts.configuration = getattr(args, 'configuration', 'release')
    opts.build_dir = args.build_dir
    opts.archives_download_dir = args.archives_download_dir
    opts.patches_root_dir = args.patches_root_dir
    opts.tools_root_dir = args.tools_root_dir
    opts.vs_ver = args.vs_ver
    opts.vs_install_path = args.vs_install_path
    opts.python_dir = args.python_dir
    opts.msys_dir = args.msys_dir
    opts.clean = args.clean
    opts.msbuild_opts = args.msbuild_opts
    opts.no_deps = args.no_deps
    opts.check_hash = args.check_hash
    opts.skip = args.skip

    if not opts.archives_download_dir:
        opts.archives_download_dir = os.path.join(args.build_dir, 'src')
    if not opts.patches_root_dir:
        opts.patches_root_dir = sys.path[0]
    if not opts.tools_root_dir:
        opts.tools_root_dir = os.path.join(args.build_dir, 'tools')
    if not opts.vs_install_path:
        opts.vs_install_path = r'C:\Program Files (x86)\Microsoft Visual Studio %s.0' % (opts.vs_ver,)

    opts.projects = args.project

    for p in opts.projects:
        if not p in Project.get_names():
            error_exit(
                p + " is not a valid project name, available projects are:\n\t" + "\n\t".join(Project.get_names()))

    return opts

def __get_projects_to_build(opts):
    to_build = ordered_set()
    for name in opts.projects:
        p = Project.get_project(name)
        if not opts.no_deps:
            for dep in p.all_dependencies:
                to_build.add(dep)
        to_build.add(p)

    # See if we need to drop some project
    if opts.skip:
        to_skip = opts.skip.split(',')
        for s in to_skip:
            if not s in Project.get_names():
                error_exit(
                    s + " is not a valid project name, available projects are:\n\t" + "\n\t".join(Project.get_names()))

            p = Project.get_project(s)
            if p in to_build:
                print_debug('Dropped project %s' % (s, ))
                to_build.remove(p)
    return to_build

def do_build(args):
    opts = get_options(args)
    print_debug("options are: %s" % (opts.__dict__,))
    builder = Builder(opts)
    builder.preprocess()

    to_build = __get_projects_to_build(opts)
    if not to_build:
        error_exit("nothing to do")
    print_debug("building %s" % ([p.name for p in to_build],))

    builder.build(to_build)

def do_list(args):
    def do_list_type(type, desc):
        nl = [x.name for x in Project._projects if x.type == type]
        if nl:
            nl.sort()
            print("%s:\n\t" % (desc, ) + "\n\t".join(nl))
    do_list_type(GVSBUILD_TOOL, "Available tools")
    do_list_type(GVSBUILD_PROJECT, "Available projects")
    do_list_type(GVSBUILD_GROUP, "Available groups")
    sys.exit(0)

def create_parser():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='Jhbuild-like system for Windows to build Gtk and friends',
        epilog=
    """
Examples:
    build.py build libpng libffi
        Build libpng, libffi, and their dependencies (zlib).

    build.py build --no-deps glib
        Build glib only.

    build.py build --skip gtk,pycairo,pygobject,pygtk all
        Build everything except gtk, pycairo
    """)

    #==============================================================================
    # Global options
    #==============================================================================

    parser.add_argument('-v', '--verbose', default=False, action='store_true',
                        help='Print lots of stuff.')
    parser.add_argument('-d', '--debug', default=False, action='store_true',
                        help='Print even more stuff.')

    subparsers = parser.add_subparsers()

    #==============================================================================
    # build
    #==============================================================================

    p_build = subparsers.add_parser('build', help='build project(s)')
    p_build.set_defaults(func=do_build)

    p_build.add_argument('-p', '--platform', default='x86', choices=['x86', 'x64'],
                         help='Platform to build for, x86 or x64. Default is x86.')
    p_build.add_argument('-c', '--configuration', default='release', choices=['release', 'debug'],
                         help='Configuration to build, release or debug. Default is release.')
    p_build.add_argument('--build-dir', default=r'C:\gtk-build',
                         help='The directory where the sources will be downloaded and built.')
    p_build.add_argument('--msys-dir', default=r'C:\Msys64',
                         help='The directory where you installed msys2.')
    p_build.add_argument('--archives-download-dir',
                         help="The directory to download the source archives to. It will be created. " +
                              "If a source archive already exists here, it won't be downloaded again. " +
                              "Default is $(build-dir)\\src.")
    p_build.add_argument('--patches-root-dir',
                         help="The directory where you checked out https://github.com/wingtk/gvsbuild.git. Default is $(build-dir)\\github\\gvsbuild.")
    p_build.add_argument('--tools-root-dir',
                         help="The directory where to install the downloaded tools. Default is $(build-dir)\\tools.")
    p_build.add_argument('--vs-ver', default='12',
                         help="Visual Studio version 10,12,14, etc. Default is 12.")
    p_build.add_argument('--vs-install-path',
                         help=r"The directory where you installed Visual Studio. Default is 'C:\Program Files (x86)\Microsoft Visual Studio $(build-ver).0'")
    p_build.add_argument('--python-dir', default=os.path.dirname(sys.executable),
                         help="The directory where you installed python.")

    p_build.add_argument('--check-hash', default=False, action='store_true',
                         help='Only check hashes of downloaded archive(s), no build')
    p_build.add_argument('--clean', default=False, action='store_true',
                         help='Build the project(s) from scratch')
    p_build.add_argument('--no-deps', default=False, action='store_true',
                         help='Do not build dependencies of the selected project(s)')

    p_build.add_argument('--msbuild-opts', default='',
                         help='Command line options to pass to msbuild.')

    p_build.add_argument('--skip', default='',
                         help='A comma separated list of project(s) not to builded.')

    p_build.add_argument('project', nargs='+',
                         help='Project(s) to build.')

    #==============================================================================
    # list
    #==============================================================================

    p_list = subparsers.add_parser('list', help='list available projects')
    p_list.set_defaults(func=do_list)

    return parser
