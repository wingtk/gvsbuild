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

gperf_sources = [
  'version.cc',
  'positions.cc',
  'options.cc',
  'keyword.cc',
  'keyword-list.cc',
  'input.cc',
  'bool-array.cc',
  'hash-table.cc',
  'search.cc',
  'output.cc',
  'main.cc',
]

gperf_exe = executable('gperf', gperf_sources,
  include_directories: gperf_incs,
  dependencies: libm,
  link_with: libgp,
  native: true,
  install: not meson.is_subproject())

if meson.is_subproject()
  meson.override_find_program('gperf', gperf_exe)
endif
