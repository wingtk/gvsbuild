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
import ctypes

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

# Original windows console title
_script_org_title = None
def script_title(new_title):
    """
    Set the new console title for the running script, saving the old one

    Passing None to the title restores the old, saved, one
    """

    global  _script_org_title
    if new_title:
        # Save the old title
        if _script_org_title is None:
            buf = ctypes.create_unicode_buffer(256)
            ctypes.windll.kernel32.GetConsoleTitleW(buf, 256)
            _script_org_title = buf.value
        ctypes.windll.kernel32.SetConsoleTitleW('gvsbuild ' + new_title)
    else:
        # Restore old title
        if _script_org_title is not None:
            ctypes.windll.kernel32.SetConsoleTitleW(_script_org_title)
            # cleanup if we want to call the function again
            _script_org_title = None
