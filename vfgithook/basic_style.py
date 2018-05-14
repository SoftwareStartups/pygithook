""" this module tests for coding style issues in many different text files """

import re
import os
import sys

from . import githook

MAX_LINE_LENGTH = 90
TABS = re.compile(r'(\t+)')
TRAIL = re.compile(r'([ \t]+)$')

LANG_TYPES = ['ml', 'mli', 'mly', 'mll',
              'py', 'lint',
              'hh', 'hpp', 'hxx', 'h++', 'cc', 'cpp', 'cxx', 'c++',
              'c', 'h',
              'cs',
              'css', 'js', 'jsx',
              'java', 'scala',
              'sol']

CHECKLENGTHMAGIC = '__GITHOOK_IGNORE_LONGLINE'


def _check_file(filename):
    "return True if the filename can be checked"
    _basename, extension = os.path.splitext(filename)
    return extension.lstrip('.') in LANG_TYPES


def _linelen(line, tabsize=8):
    """ Calculate the length of aline, considering tabsize """
    tab_cnt = line.count('\t')
    if not tab_cnt:
        return len(line)

    count = 0
    for char in line:
        if char == '\t':
            count += tabsize - count % tabsize
        else:
            count += 1

    return count

# pylint: disable=too-few-public-methods

class ValidationStats(object):
    """ Class for accumulating error statistics """

    def __init__(self):
        self.toolong = 0
        self.tabs = 0
        self.trailwhite = 0
        self.cret = 0

    def __nonzero__(self):
        """
        Override nonzero check
        """
        return self.toolong or self.tabs or \
               self.trailwhite or self.cret

def _validate(changeset_info, filename, stats, exit_code):
    """
    Check a file for simple styling issues
    """
    def msg(lineno, _line, message):
        """ Print a message """
        print '%s:%d> %s' % (filename, lineno + 1, message)

    def bad():
        """ To be called when we find a styling violation """
        if exit_code is not None:
            sys.exit(exit_code)
    content = changeset_info.current_content(filename)

    if content is None:
        return

    staged_lines = content.split('\n')

    check_length = True

    for i, line in enumerate(staged_lines):
        # skip line length checks if the magic word is found
        if CHECKLENGTHMAGIC in line:
            check_length = False

        line = line.rstrip('\n')

        # no carriage returns
        if line.find('\r') != -1:
            stats.cret += 1
            msg(i, line, 'carriage return found')
            bad()

        # lines max out at MAX_LINE_LENGTH chars
        llen = _linelen(line)
        if check_length and llen > MAX_LINE_LENGTH:
            stats.toolong += 1
            msg(i, line, 'line too long (%d chars)' % llen)
            bad()

        # no tabs used to indent
        match = TABS.search(line)
        if match:
            stats.tabs += 1
            msg(i, line, 'using tabs')
            bad()

        # no trailing whitespace
        if TRAIL.search(line):
            stats.trailwhite += 1
            msg(i, line, 'trailing whitespace')
            bad()


def _check_format(filename, changeset_info):
    """
    Check file formatting for a specific file, returns whether there were any
    violations.
    """
    errors = ValidationStats()
    _validate(changeset_info, filename, errors, None)
    return not errors # no errors found


class BasicStyleHook(githook.GitHook):
    """ Basic hooks to check basic coding style metrics """

    def should_check_file(self, filename):
        return _check_file(filename)

    def check_file(self, changeset_info, filename):
        return _check_format(filename, changeset_info)
