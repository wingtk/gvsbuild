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

"""gvsbuild deps print / .gv graph."""

import gvsbuild.groups  # noqa: F401
import gvsbuild.projects  # noqa: F401
import gvsbuild.tools  # noqa: F401
from gvsbuild.utils.base_project import Project, ProjectType
from gvsbuild.utils.utils import ordered_set


def print_deps(flatten=False, add_all=False):
    done = []

    def dump_single_dep(st, name, flatten):
        if flatten:
            if not st:
                done.append(name)
        else:
            if st:
                # dependency
                print(f"{st}{name}")
            else:
                print(f"  > {name}")
                st = "   "
            done.append(name)

        rt = False
        p = Project._dict[name]
        if p.dependencies:
            for d in p.dependencies:
                add = True
                if not add_all:
                    ty = Project._dict[d].type
                    if ty != ProjectType.PROJECT:
                        add = False

                if add:
                    rt = True
                    if d in done:
                        if not flatten:
                            print(f"{st}    {d} *")
                    else:
                        done.append(d)
                        dump_single_dep(f"{st}    ", d, flatten)
        return rt

    prj = [x.name for x in Project._projects if x.type == ProjectType.PROJECT]
    print("Projects dependencies:")
    for n in prj:
        done = []
        if flatten:
            print(f"> {n}")
        if dump_single_dep("", n, flatten):
            if flatten:
                done.remove(n)
                for t in sorted(done):
                    print(f"    {t}")

            else:
                print("")


def make_graph(
    out_file,
    put_all=False,
    invert_dep=False,
    add_tools=False,
    add_groups=False,
    skip=None,
):
    gr_colors = [
        0x000080,
        0x008000,
        0x008080,
        0x800000,
        0x800080,
        0x808000,
        0x808080,
        0x0000F0,
        0x00F000,
        0x00F0F0,
        0xF00000,
        0xF000F0,
        0xF0F000,
        0xF00080,
        0xF08000,
        0xF08080,
        0x80F000,
        0x80F080,
        0x00F080,
        0x0080F0,
        0x8000F0,
        0x8080F0,
    ]
    gr_index = 0

    to_skip = set(skip)
    with open(out_file, "w", encoding="utf-8") as fo:
        print(f"Writing file {out_file}")
        used = set()
        fo.write("digraph gtk3dep {\n")
        for n in Project._names:
            if n not in to_skip:
                t = Project._dict[n]

                add = True
                if t.type == ProjectType.TOOL:
                    add = add_tools
                elif t.type == ProjectType.GROUP:
                    add = add_groups
                else:
                    add = True

                if add:
                    if t.dependencies:
                        gr_index += 1
                        gr_index %= len(gr_colors)
                        for d in t.dependencies:
                            if d in to_skip:
                                print(f"Skip '{d}' for '{n}'")
                            else:
                                if invert_dep:
                                    fo.write(
                                        f'    "{d}" -> "{n}" [color="#{gr_colors[gr_index]:06x}"];\n'
                                    )
                                else:
                                    fo.write(
                                        f'    "{n}" -> "{d}" [color="#{gr_colors[gr_index]:06x}"];\n'
                                    )
                                used.add(d)
                else:
                    used.add(t.name)

        if put_all:
            # Puts all projects that are not referenced from others
            for n in Project._names:
                if n not in used:
                    fo.write(f'    "BUILD" -> "{n}" [color="#c00080"];\n')

        fo.write("};\n")


def compute_deps(proj):
    if hasattr(proj, "all_dependencies"):
        return
    dependencies = ordered_set()
    for dep in proj.dependencies:
        compute_deps(dep)
        for p in dep.all_dependencies:
            dependencies.add(p)
        dependencies.add(dep)
    proj.all_dependencies = dependencies


def deps(
    flatten: bool = False,
    dep_tools: bool = False,
    graph: bool = False,
    graph_all: bool = False,
    add_tools: bool = False,
    add_groups: bool = False,
    gv_file: str = "wingtk.gv",
    invert: bool = False,
    skip: list[str] | None = None,
):
    """Show project dependencies.

    Args:
        flatten: Flatten the dependencies.
        dep_tools: Include tools in the dependencies.
        graph: Generate a graphviz file.
        graph_all: Also include unreferenced projects to the graph.
        add_tools: Include tools in the graph.
        add_groups: Include group projects in the graph.
        gv_file: Graphviz output file.
        invert: Invert the dependencies.
        skip: A comma separated list of projects not to graph.
    """
    Project.add_all()
    # do what's asked
    if graph:
        # .gv graph
        make_graph(
            out_file=gv_file,
            put_all=graph_all,
            invert_dep=invert,
            add_tools=add_tools,
            add_groups=add_groups,
            skip=skip,
        )
    else:
        # simple dep print
        print_deps(flatten=flatten, add_all=dep_tools)
