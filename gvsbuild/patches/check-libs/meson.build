# Copyright (C) 2017 - Daniele Forghieri
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.

# This (very) simple project just uses a library, getting the dependencies
# with pkg-config, and prints the name & address of one, single, library's
# symbol.
#
# It's not meant to replace the internal tests that each (good) library should
# have or exercise any function or operation of the software, only see if it
# compile, link and execute.
#
# Is only used to check if the pkg-config .pc files are correct and the
# library can be used outside the internal build (when the include files are
# normally visible without problem).
#

project('check-libs', 'c',
        version: '0.1.0',
        default_options: [
          'buildtype=debugoptimized',
          'warning_level=1',
        ],
        meson_version : '>= 0.42')

# Set to false if you want to skip not found library, please use only in test :)
check_all = true

# atk
atk_required_ver = '>= 2.24.0'
atk_dep = dependency('atk', version: atk_required_ver, required: check_all)
if atk_dep.found()
        test_atk = executable('test_atk',
                                [ 'test_atk.c', 'check_utils.c', ],
                               dependencies: [ atk_dep, ],
                                )

        test('atk', test_atk)
endif

# cairo
cairo_required_ver = '>= 1.15.2'
cairo_dep = dependency('cairo', version: cairo_required_ver, required: check_all)
if cairo_dep.found()
        test_cairo = executable('test_cairo',
                                     [ 'test_cairo.c', 'check_utils.c', ],
                                     dependencies: [ cairo_dep, ],
                                    )

        test('cairo', test_cairo)
endif

# freetype2
freetype2_required_ver = '>= 2.7.1'
freetype2_dep = dependency('freetype2', version: freetype2_required_ver, required: check_all)
if freetype2_dep.found()
        test_freetype2 = executable('test_freetype2',
                                    [ 'test_freetype2.c', 'check_utils.c', ],
                                    dependencies: [ freetype2_dep, ],
                                   )

        test('freetype2', test_freetype2)
endif

# libarchive
libarchive_required_ver = '>= 3.3.1'
libarchive_dep = dependency('libarchive', version: libarchive_required_ver, required: check_all)
if libarchive_dep.found()
        test_libarchive = executable('test_libarchive',
                                     [ 'test_libarchive.c', 'check_utils.c', ],
                                     dependencies: [ libarchive_dep, ],
                                    )

        test('libarchive', test_libarchive)
endif

# curl
libcurl_required_ver = '>= 7.54.0'
libcurl_dep = dependency('libcurl', version: libcurl_required_ver, required: check_all)
if libcurl_dep.found()
        test_libcurl = executable('test_libcurl',
                                [ 'test_libcurl.c', 'check_utils.c', ],
                               dependencies: [ libcurl_dep, ],
                                )
        test('libcurl', test_libcurl)
endif

# ffi
libffi_required_ver = '>= 3.2.1'
libffi_dep = dependency('libffi', version: libffi_required_ver, required: check_all)
if libffi_dep.found()
        test_libffi = executable('test_libffi',
                                [ 'test_libffi.c', 'check_utils.c', ],
                               dependencies: [ libffi_dep, ],
                                )
        test('libffi', test_libffi)
endif


# gdk-pixbuf
gdk_pixbuf_required_ver = '>= 2.36.10'
gdk_pixbuf_dep = dependency('gdk-pixbuf-2.0', version: gdk_pixbuf_required_ver, required: check_all)
if gdk_pixbuf_dep.found()
        test_gdk_pixbuf = executable('test_gdk-pixbuf',
                                     [ 'test_gdk-pixbuf.c', 'check_utils.c', ],
                                     dependencies: [ gdk_pixbuf_dep, ],
                                    )

        test('gdk-pixbuf', test_gdk_pixbuf)
endif

# glib
glib_required_ver = '>= 2.54.2'
glib_dep = dependency('glib-2.0', version: glib_required_ver, required: check_all)
if glib_dep.found()
        test_glib = executable('test_glib',
                                     [ 'test_glib.c', 'check_utils.c', ],
                                     dependencies: [ glib_dep, ],
                                    )

        test('glib', test_glib)
endif

# jasper
jasper_required_ver = '>= 2.0.12'
jasper_dep = dependency('jasper', version: jasper_required_ver, required: check_all)
if jasper_dep.found()
        test_jasper = executable('test_jasper',
                                 [ 'test_jasper.c', 'check_utils.c', ],
                                 dependencies: [ jasper_dep, ],
                                )

        test('jasper', test_jasper)
endif

# json-glib
json_glib_required_ver = '>= 1.4.2'
json_glib_dep = dependency('json-glib-1.0', version: json_glib_required_ver, required: check_all)
if json_glib_dep.found()
        test_json_glib = executable('test_json_glib',
                                 [ 'test_json_glib.c', 'check_utils.c', ],
                                 dependencies: [ json_glib_dep, ],
                                )

        test('json_glib', test_json_glib)
endif


# libjpeg
libjpeg_required_ver = '>= 2.0'
libjpeg_dep = dependency('libjpeg', version: libjpeg_required_ver, required: check_all)
if libjpeg_dep.found()
        test_libjpeg = executable('test_libjpeg',
                                 [ 'test_libjpeg.c', 'check_utils.c', ],
                                 dependencies: [ libjpeg_dep, ],
                                )

        test('libjpeg', test_libjpeg)
endif

# libjpeg_turbo
libjpeg_turbo_required_ver = '>= 1.5.1'
libjpeg_turbo_dep = dependency('libturbojpeg', version: libjpeg_turbo_required_ver, required: check_all)
if libjpeg_turbo_dep.found()
        test_libjpeg_turbo = executable('test_libjpeg-turbo',
                                 [ 'test_libjpeg-turbo.c', 'check_utils.c', ],
                                 dependencies: [ libjpeg_turbo_dep, ],
                                )

        test('libjpeg-turbo', test_libjpeg_turbo)
endif

# libpng
libpng_required_ver = '>= 1.6.29'
libpng_dep = dependency('libpng', version: libpng_required_ver, required: check_all)
if libpng_dep.found()
        test_libpng = executable('test_libpng',
                                 [ 'test_libpng.c', 'check_utils.c', ],
                                 dependencies: [ libpng_dep, ],
                                )

        test('libpng', test_libpng)
endif

# libtiff
libtiff_required_ver = '>= 4.0.8'
libtiff_dep = dependency('libtiff-4', version: libtiff_required_ver, required: check_all)
if libtiff_dep.found()
        test_libtiff = executable('test_libtiff-4',
                                 [ 'test_libtiff-4.c', 'check_utils.c', ],
                                 dependencies: [ libtiff_dep, ],
                                )

        test('libtiff-4', test_libtiff)
endif

# libxml2
libxml2_required_ver = '>= 2.9.8'
libxml2_dep = dependency('libxml-2.0', version: libxml2_required_ver, required: check_all)
if libxml2_dep.found()
        test_libxml2 = executable('test_libxml2',
                                 [ 'test_libxml2.c', 'check_utils.c', ],
                                 dependencies: [ libxml2_dep, ],
                                )

        test('libxml2', test_libxml2)
endif

# libyuv
libyuv_required_ver = '>= 0.0.1724'
libyuv_dep = dependency('libyuv', version: libyuv_required_ver, required: check_all)
if libyuv_dep.found()
        test_libyuv = executable('test_libyuv',
                                [ 'test_libyuv.c', 'check_utils.c', ],
                               dependencies: [ libyuv_dep, ],
                                )
        test('libyuv', test_libyuv)
endif

# pango
pango_required_ver = '>= 1.40.14'
pango_dep = dependency('pango', version: pango_required_ver, required: check_all)
if pango_dep.found()
        test_pango = executable('test_pango',
                                     [ 'test_pango.c', 'check_utils.c', ],
                                     dependencies: [ pango_dep, ],
                                    )

        test('pango', test_pango)
endif

# wing
wing_required_ver = '>= 0.104'
wing_dep = dependency('wing-1.0', version: wing_required_ver, required: check_all)
if wing_dep.found()
        test_wing = executable('test_wing',
                                [ 'test_wing.c', 'check_utils.c', ],
                               dependencies: [ wing_dep, ],
                                )

        test('wing', test_wing)
endif

# zlib
zlib_required_ver = '>= 1.2.11'
zlib_dep = dependency('zlib', version: zlib_required_ver, required: check_all)
if zlib_dep.found()
        test_zlib = executable('test_zlib',
                                [ 'test_zlib.c', 'check_utils.c', ],
                               dependencies: [ zlib_dep, ],
                                )

        test('zlib', test_zlib)
endif
