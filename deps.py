#  Copyright (C) 2017 - Daniele Forghieri
#  Copyright (C) 2020 - Daniel F. Dickinson
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
#

"""
gvsbuild deps print / .gv graph
"""
# Verify we can import from the script directory
try:
    import gvsbuild.utils.utils
except ImportError:
    # We are probably using an embedded installation
    print('Error importing utility (running the embedded interpreter ?), fixing paths ...')
    import sys
    import os
    # Get the script dir
    script_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
    # and add it at the beginning, emulating the standard python startup
    sys.path.insert(0, script_dir)

import argparse

from gvsbuild.utils.base_project import Project, GVSBUILD_GROUP, GVSBUILD_TOOL, GVSBUILD_PROJECT, GVSBUILD_APPLICATION
from gvsbuild.utils.utils import ordered_set
# All default tools ...
import gvsbuild.tools
# projects ...
import gvsbuild.projects
# ... and groups
import gvsbuild.groups
# ... and applications
import gvsbuild.applications

def print_deps(flatten=False, add_all=False, no_applications=False):
    done = []

    def dump_single_dep(st, name, flatten):
        if flatten:
            if not st:
                done.append(name)
        else:
            if st:
                # dependency
                print("%s%s" % (st, name, ))
            else:
                print("  > %s" % (name, ))
                st = "   "
            done.append(name)

        rt = False
        p = Project._dict[name]
        if p.dependencies:
            for d in p.dependencies:
                add = True
                if not add_all:
                    ty = Project._dict[d].type
                    if ty != GVSBUILD_PROJECT:
                        add = False
                    if (ty == GVSBUILD_APPLICATION) and (not no_applications):
                        add = True

                if add:                        
                    rt = True
                    if d in done:
                        if not flatten:
                            print("%s    %s *" % (st, d, ))
                    else:
                        done.append(d)
                        dump_single_dep(st + "    ", d, flatten)
        return rt

    prj = [ x.name for x in Project._projects if x.type == GVSBUILD_PROJECT ]
    print("Projects dependencies:")
    for n in prj:
        done = []
        if flatten:
            print("> %s" % (n, ))
        if dump_single_dep("", n, flatten):
            if flatten:
                done.remove(n)
                for t in sorted(done):
                    print("    %s" % (t, ))

            else:
                print('')

    if not no_applications:
        apps = [ x.name for x in Project._projects if x.type == GVSBUILD_APPLICATION ]
        print("Application dependencies:")
        for n in apps:
            done = []
            if flatten:
                print("> %s" % (n, ))
            if dump_single_dep("", n, flatten):
                if flatten:
                    done.remove(n)
                    for t in sorted(done):
                        print("    %s" % (t, ))

                else:
                    print('')

def make_graph(out_file, put_all = False, invert_dep = False, add_tools = False, add_groups = False, no_applications = False, skip = ''):
    gr_colors = [
        0x000080,   0x008000,   0x008080,   0x800000,
        0x800080,   0x808000,   0x808080,   0x0000f0,
        0x00f000,   0x00f0f0,   0xf00000,   0xf000f0,
        0xf0f000,   0xf00080,   0xf08000,   0xf08080,
        0x80f000,   0x80f080,   0x00f080,   0x0080f0,
        0x8000f0,   0x8080f0 ]
    gr_index = 0

    to_skip = set(skip.split(','))
    with open(out_file, "wt") as fo:
        print('Writing file %s' % (out_file, ))
        used = set()
        fo.write('digraph gtk3dep {\n')
        for n in Project._names:
            if n not in to_skip:
                t = Project._dict[n]

                add = True
                if t.type == GVSBUILD_TOOL:
                    add = add_tools
                elif t.type == GVSBUILD_GROUP:
                    add = add_groups
                elif t.type == GVSBUILD_APPLICATION:
                    add = not no_applications
                else:
                    add = True

                if add:
                    if t.dependencies:
                        gr_index += 1
                        gr_index %= len(gr_colors)
                        for d in t.dependencies:
                            if d in to_skip:
                                print("Skip '%s' for '%s'" % (d, n, ))
                            else:
                                if invert_dep:
                                    fo.write('    "%s" -> "%s" [color="#%06x"];\n' % (d, n, gr_colors[gr_index], ))
                                else:
                                    fo.write('    "%s" -> "%s" [color="#%06x"];\n' % (n, d, gr_colors[gr_index], ))
                                used.add(d)
                else:
                    used.add(t.name)

        if put_all:
            # Puts all projects that are not referenced from others
            for n in Project._names:
                if n not in used:
                    fo.write('    "%s" -> "%s" [color="#c00080"];\n' % ('BUILD', n, ))

        fo.write('};\n')

def compute_deps(proj):
    if hasattr(proj, 'all_dependencies'):
        return
    deps = ordered_set()
    for dep in proj.dependencies:
        compute_deps(dep)
        for p in dep.all_dependencies:
            deps.add(p)
        deps.add(dep)
    proj.all_dependencies = deps

def main():
    parser = argparse.ArgumentParser(description = "Gvsbuild dependency print / analyze")

    group = parser.add_argument_group('Dependencies print (default)')
    # Simple dep dump
    group.add_argument('-f', '--flatten', default=False, action='store_true',
                         help='Flatten (and sort) the dependencies dump of the single project.')
    group.add_argument('--dep-tools', default=False, action='store_true',
                         help='Add also the tool projects.')

    # .gv (dot) graph of dependencies
    group = parser.add_argument_group('Graph file (.gv, dot format) of the dependencies')
    group.add_argument('-g', '--graph', default=False, action='store_true',
                         help='Create a .gv graph of the dependencies.')
    group.add_argument('-a', '--all', default=False, action='store_true',
                         help='Graph: add also all unreferenced projects to the graph.')
    group.add_argument('--add-tools', default=False, action='store_true',
                         help='Graph: add also the tool projects.')
    group.add_argument('--add-groups', default=False, action='store_true',
                         help='Graph: add also the group projects.')
    group.add_argument('--no-applications', default=False, action='store_true',
                         help='Graph: do not also add the application projects.')
    group.add_argument('-o', '--gv-file', default='wingtk.gv',
                        help='Graph: output file name.')
    group.add_argument('-i', '--invert', default=False, action='store_true',
                         help='Graph: invert the dependency track.')
    group.add_argument('--skip', default='',
                         help='A comma separated list of project(s) not to handle.')

    # get the option(s)
    opt = parser.parse_args()
    # now add the tools/projects/groups
    Project.add_all()
    # do what's asked
    if opt.graph:
        # .gv graph
        make_graph(out_file=opt.gv_file,
                   put_all=opt.all,
                   invert_dep=opt.invert,
                   add_tools=opt.add_tools,
                   add_groups=opt.add_groups,
                   no_applications=opt.no_applications,
                   skip=opt.skip,
                   )
    else:
        # simple dep print
        print_deps(flatten=opt.flatten,
                   add_all=opt.dep_tools,
                   no_applications=opt.no_applications,
                   )

if __name__ == '__main__':
    main()
