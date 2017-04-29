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
Simple user interface for info, log & debug messages
"""

import sys

global_verbose = False
global_debug = False

def print_message(msg):
    print(msg)

def print_log(msg):
    if global_verbose:
        print(msg)

def print_debug(msg):
    if global_debug:
        print("Debug:", msg)

def error_exit(msg):
    print("Error:", msg, file=sys.stderr)
    sys.exit(1)

def handle_global_options(args):
    global global_verbose
    global global_debug
    if args.verbose:
        global_verbose = True
    if args.debug:
        global_verbose = True
        global_debug = True
