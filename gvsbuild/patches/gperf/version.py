#!/usr/bin/env python3
#
# gperf version.py
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
#
# Extracts version from src/version.cc, because like any sane build system
# we extract the version from the code instead of having the build system set
# the version for the code to consume.

import os
import sys

version = None

srcroot = os.path.dirname(__file__)

f = open(os.path.join(srcroot, "src/version.cc"))

for line in f:
    if line.startswith("const char *version_string"):
        version = line[26:].split('"')[1]
        break

f.close()

if not version:
    print(
        "Warning: Could not extract version from src/version.cc in",
        srcroot,
        file=sys.stderr,
    )
    sys.exit(-1)

print(version)
sys.exit(0)
