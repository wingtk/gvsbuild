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
import os
import datetime
import ctypes
from contextlib import contextmanager

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

# Log levels
LOG_ALWAYS = 1
LOG_VERBOSE = 2
LOG_DEBUG = 3

class LogElem(object):
    def __init__(self, msg, enabled, tim=None):
        self.msg = msg
        self.tim = tim if tim else datetime.datetime.now()
        self.indent = not enabled
        self.enabled = enabled

class Log(object):
    """"
    Simple log class, used mainly to time the execution of the script
    """
    _verbose = False
    _debug = False
    def __init__(self):
        self.st_time = datetime.datetime.now()
        self.fo = None
        self.level = LOG_ALWAYS 

    def configure(self, file_path, opts=None):
        max_size_kb = 0
        single = False
        if opts:
            if opts.debug:
                self._verbose = True
                self._debug = True
                self.level = LOG_DEBUG
            elif opts.verbose:
                self._verbose = True
                self.level = LOG_VERBOSE
            max_size_kb = opts.log_size
            single = opts.log_single
            self.capture = opts.capture_out
            if single:
                max_size_kb = 0

        if file_path:
            if not os.path.exists(file_path):
                created = True
                os.makedirs(file_path)
            else:
                created = False
                
            if single:
                file_name = self.st_time.strftime('gvsbuild-log-%Y%m%d-%H%M%S.txt')
            else:
                file_name = 'gvsbuild-log.txt'

            self.log_file = os.path.join(file_path, file_name)
            if max_size_kb:
                try:
                    c_size = os.path.getsize(self.log_file) / 1024
                except Exception as e:
                    print('Exception reading log file size (%s)', self.log_file)
                    print(e)
                    c_size = 0
                
                if c_size > max_size_kb:
                    old_file = os.path.join(file_path, 'gvsbuild-log.old.txt')
                    try:
                        os.remove(old_file)
                    except FileNotFoundError:
                        pass
                    os.rename(self.log_file, old_file)
                
            self.operations = []
            self.fo = open(self.log_file, 'at')
            self._output('Script started')
            if created:
                self.log("Log directory %s created" % (file_path, ))
            if opts and not self._debug:
                # Dump some information
                self._output_val('Configuration', opts.configuration )
                self._output_val('Platform', opts.platform)
                self._output_val('Vs ver', opts.vs_ver)
                self._output_val('Vs path', opts.vs_install_path)
                self._output_val('Sdk ver', opts.win_sdk_ver)

    def _get_delta(self, start, end=None):
        if not end:
            end = datetime.datetime.now()
        dt = datetime.datetime.now() - start
        return '%u.%03u' % (dt.seconds, dt.microseconds / 1000, )

    def _indend_check(self):
        if self.operations:
            co = self.operations[-1]
            if not co.indent:
                # not yet logged
                self.operations.pop()
                self._output('%s ...' % (co.msg, ), check_indent=False)
                co.indent = True
                self.operations.append(co)

    def close(self):
        while self.operations:
            self.end()
            
        self._output('Script ended correctly (%s s)' % (self._get_delta(self.st_time), ))
        # The \n is correct, to separate other build's logs
        self._output('--------\n')
        self.fo.close()
        self.fo = None

    def start(self, msg, level=LOG_ALWAYS):
        enabled = level <= self.level
        if enabled:
            print(msg)
            self._indend_check()

        if self.capture:
            self._output(msg, check_indent=False)

        co = LogElem(msg, enabled)
        self.operations.append(co)

    def start_verbose(self, msg):
        self.start(msg, level=LOG_VERBOSE)
        
    def start_debug(self, msg):
        self.start(msg, level=LOG_DEBUG)

    def end(self, force_print=False, mark_error=False):
        if self.operations:
            co = self.operations.pop()
            if co.enabled:
                if mark_error:
                    out_msg = '*** Error: %s (%s s)' % (co.msg, self._get_delta(co.tim), )
                else:
                    out_msg = '%s - Ended in %s s' % (co.msg, self._get_delta(co.tim), )
                self._output(out_msg, check_indent=False)
                if force_print:
                    print(out_msg)
                if not self.operations:
                    self.flush()

    def flush(self):
        if self.fo:
            self.fo.flush()

    def _output(self, msg, add_date=True, check_indent=True):
        if self.fo:
            if check_indent:
                self._indend_check()
            msg = ' ' * len(self.operations) * 2 + msg
            if add_date:
                now_val = datetime.datetime.now()
                self.fo.write('%s %s\n' % (now_val.strftime('%Y-%m-%d %H:%M:%S'), msg, ))
            else:
                self.fo.write('%19s %s\n' % ('', msg, ))
            return False
        else:
            print(msg)
            # tell the caller we already print on video
            return True

    def _output_val(self, msg, val):
        self._output('%16s: %s' % (msg, val, ))

    def message_indent(self, msg):
        if self._output(msg, add_date=False):
            return
        print('  %s' % (msg, ))

    def message(self, msg):
        if self._output(msg):
            # already printed
            return
        print(msg)

    def messages_dump(self, msgs, prt=False, err=None):
        if err is not None:
            if not err:
                err = 'Attention! Error presents!'
            self.message(err)
            self.message('')
            # with error we want to know what's happeninh
            prt = True

        lines = msgs.split('\n')
        lines = [l.rstrip() for l in lines if l.rstrip() != '']
        if self.fo:
            # On the file, if active
            for l in lines:
                self.fo.write('    %s\n' % (l, ))
        
        if prt:
            for l in lines:
                print(l) 

    def log(self, msg):
        if self._verbose:
            if self._output(msg):
                return
            print(msg)
        elif self.fo:
            self._output(msg)

    def debug(self, msg):
        if self._debug:
            if self._output(msg):
                return
            print('Debug:', msg)
        elif self.fo:
            self._output(msg)

    def verbose_on(self):
        return self._verbose

    def debug_on(self):
        return self._debug

    def error_exit(self, msg):
        self._output('Error:' + msg)
        print("Error:", msg, file=sys.stderr)
        sys.exit(1)

    @staticmethod
    @contextmanager
    def simple_oper(msg, level=LOG_ALWAYS):
        '''
        To time single operation, using:
        with log.simple_oper('timing ...'):
           .. do stuff
        '''
        log.start(msg, level)
        yield True
        log.end()

# single instance of the log class
log = Log()

if __name__ == '__main__':
    import time
    
    log.configure('.', None)
    log.start('Test #1')
    time.sleep(.8)
    log.start('Test #2, nested')
    time.sleep(.5)
    log.end()
    with log.simple_oper('Test with context manager') as l:
        time.sleep(0.35)
        with log.simple_oper('Second test with context manager'):
            time.sleep(0.15)
    # log.end()
    log.close()
    
