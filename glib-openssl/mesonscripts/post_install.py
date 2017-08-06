#!/usr/bin/env python3

import os
import subprocess

# Packagers handle this
if 'DESTDIR' not in os.environ:
    # post install scripts can't pass these so we must check again
    ret = subprocess.check_output(('pkg-config', '--variable',
                                   'giomoduledir', 'gio-2.0'))
    moduledir = ret.decode().strip()
    print('Updating module cache in {}...'.format(moduledir))
    subprocess.check_call(('gio-querymodules', moduledir))
