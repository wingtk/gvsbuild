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

import re
import sys
from typing import Any, Tuple, Union

from gvsbuild.utils.base_project import Project, ProjectType, get_project_by_type


def separate_name_and_major_version(name: str) -> Tuple[Union[str, Any], ...]:
    # Exceptions where ending with a simple digit is part of the library name
    if name in {"nghttp2", "ssh2", "libxml2", "libtiff-4"}:
        return name, None
    # https://regex101.com/r/1c4iLx/2
    match = re.search(r"([a-z-]*\d{3}|[a-z-]*\d{0})(\d$)?", name)
    return match.group(1, 2) if match else (None, None)


def outdated():
    try:
        import lastversion
        from packaging import version
    except ImportError:
        print("Please pip install lastversion in your Python environment")
        sys.exit(0)

    Project.add_all()
    projects = get_project_by_type(ProjectType.PROJECT)
    projects.extend(get_project_by_type(ProjectType.TOOL))
    print("Looking for projects and tools that are out-of-date, please submit a PR!")
    print(f"\t{'Project Name':<{Project.name_len}} {'Current':<45} {'Latest':<45}")
    try:
        for project in projects:
            # glib-py-wrapper and check-libs are vendored in gvsbuild
            if (
                project[0] in ("glib-py-wrapper", "check-libs", "hello-world")
                or not project[1]
            ):
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
                "librsvg": "https://gitlab.gnome.org/GNOME/librsvg",
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
        print(
            "Create or update the GITHUB token at https://github.com/settings/tokens, then set or update the token environmental variable with:\n$env:GITHUB_API_TOKEN=xxxxxxxxxxxxxxx"
        )
