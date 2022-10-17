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

projects = [
    "adwaita-icon-theme",
    "atk",
    "boringssl",
    "cairo",
    "check-libs",
    "clutter",
    "cogl",
    "cyrus-sasl",
    "dcv-color-primitives",
    "emeus",
    "enchant",
    "ffmpeg",
    "fontconfig",
    "freerdp",
    "freetype",
    "fribidi",
    "gdk-pixbuf",
    "gettext",
    "glib",
    "glib-networking",
    "glib-py-wrapper",
    "gobject-introspection",
    "graphene",
    "gsettings-desktop-schemas",
    "gst-plugins-bad",
    "gst-plugins-base",
    "gst-plugins-good",
    "gst-python",
    "gstreamer",
    "gtk2",
    "gtk3",
    "gtk4",
    "gtksourceview4",
    "gtksourceview5",
    "harfbuzz",
    "hello-world",
    "hicolor-icon-theme",
    "icu",
    "json-c",
    "json-glib",
    "leveldb",
    "lgi",
    "libadwaita",
    "libarchive",
    "libcroco",
    "libcurl",
    "libepoxy",
    "libffi",
    "libgxps",
    "libjpeg-turbo",
    "libmicrohttpd",
    "libpng",
    "libpsl",
    "librsvg",
    "libsoup2",
    "libsoup3",
    "libssh",
    "libssh2",
    "libtiff-4",
    "libuv",
    "libvpx",
    "libxml2",
    "libyuv",
    "libzip",
    "lmdb",
    "luajit",
    "lz4",
    "mit-kerberos",
    "nghttp2",
    "nv-codec-headers",
    "openh264",
    "openssl",
    "opus",
    "orc",
    "pango",
    "pixman",
    "pkg-config",
    "portaudio",
    "protobuf",
    "protobuf-c",
    "pycairo",
    "pygobject",
    "sqlite",
    "win-iconv",
    "wing",
    "x264",
    "zlib",
]
tools = [
    "cargo",
    "cmake",
    "go",
    "meson",
    "msys2",
    "nasm",
    "ninja",
    "nuget",
    "perl",
    "python",
    "yasm",
]
groups = ["all", "gtk3-full", "tools", "tools-check"]


def test_list_projects(typer_app, runner):
    result = runner.invoke(typer_app, ["list-projects"])
    assert result.exit_code == 0
    for group in groups:
        assert group in result.stdout
    for project in projects:
        assert project in result.stdout
    for tool in tools:
        assert tool in result.stdout
