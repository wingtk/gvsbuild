# meson configuration for gperf
#
# Copyright (C) 2020 Tim-Philipp Müller <tim centricular com>
#
# This file is part of GNU GPERF.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

project('gperf', 'cpp', 'c',
  version: run_command(find_program('version.py'), check: true).stdout().strip(),
  meson_version: '>= 0.49')

cxx = meson.get_compiler('cpp', native: true)

gperf_incs = include_directories('.', 'lib')

cdata = configuration_data()

libm = cxx.find_library('m', required: false)

have_dynamic_array = cxx.compiles('int func (int n) { int dynamic_array[n]; }',
  name: 'C++ compiler supports stack-allocated variable-size arrays')

cdata.set10('HAVE_DYNAMIC_ARRAY', have_dynamic_array,
  description: 'C++ compiler supports stack-allocated variable-size arrays')

subdir('lib')
subdir('src')

if not get_option('tests').disabled()
  subdir('tests')
endif

if not get_option('docs').disabled()
  subdir('doc')
endif

configure_file(output: 'config.h', configuration: cdata)
