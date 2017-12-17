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

import os
import stat
import time
import shutil
import re

from .simple_ui import print_debug

def convert_to_msys(path):
    path = path
    if path[1] != ':':
        raise Exception('oops')
    path = '/' + path[0] + path[2:].replace('\\', '/')
    return path

def _rmtree_error_handler(func, path, exc_info):
    if not os.access(path, os.W_OK):
        # Is the error an access error ?
        os.chmod(path, stat.S_IWUSR)
        func(path)
        print_debug('rmtree:read-only file/path (%s)' % (path, ))
    else:
        raise

def rmtree_full(dest_dir, retry=False):
    if retry:
        for delay in [ 0.1, 0.2, 0.4, 0.8]:
            try:
                shutil.rmtree(dest_dir, onerror=_rmtree_error_handler)
                break
            except:
                # wait a little, don't ask me why ;(
                time.sleep(delay)
    else:
        shutil.rmtree(dest_dir, onerror=_rmtree_error_handler)

def read_file(file_name):
    with open(file_name, 'rt') as fi:
        rt = [ line.rstrip('\n') for line in fi ]
    return rt

def write_file(file_name, content):
    with open(file_name, 'wt') as fo:
        for i in content:
            fo.write('%s\n' % (i, ))

def file_replace(file_name, chg_list, make_bak=True):
    """
    Execute a series of replace on the file indicated

    chg_list is an iterable of tuple (find, replace) to execute
    """

    fc = read_file(file_name)
    if make_bak:
        sv = fc
    chg = 0
    for find, repl in chg_list:
        exp = re.compile(find)
        nw = []
        for i in fc:
            nl = exp.sub(repl, i)
            if nl != i:
                chg += 1
            nw.append(nl)
        fc = nw
    if chg:
        if make_bak:
            write_file(file_name + '.bak', sv)
        write_file(file_name, fc)

class ordered_set(set):
    def __init__(self):
        set.__init__(self)
        self.__list = list()

    def add(self, o):
        if not o in self:
            set.add(self, o)
            self.__list.append(o)

    def remove(self, o):
        if o in self:
            set.remove(self, o)
            self.__list.remove(o)

    def __iter__(self):
        return self.__list.__iter__()

def python_find_libs_dir(org_dir):
    """
    From the python org_dir that can be also a virtualenv path
    return the libs dir
    """

    cur = os.path.join(org_dir, 'libs')
    if os.path.isdir(cur):
        # easy :)
        return cur

    # look for the virtualenv marker
    chk = os.path.join(org_dir, 'lib')
    if not os.path.isdir(chk):
        # one level up
        chk = os.path.join(org_dir, '..', 'lib')

    if not chk:
        # oops
        return None

    orig_file = os.path.join(chk, 'orig-prefix.txt')
    if os.path.isfile(orig_file):
        # Read and see whats happening
        with open(orig_file, 'rt') as fi:
            org_dir = fi.read()

    # Let's see if now is ok ..
    cur = os.path.join(org_dir, 'libs')
    if os.path.isdir(cur):
        return cur

    return None
