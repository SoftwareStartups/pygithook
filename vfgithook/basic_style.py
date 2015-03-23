#! /usr/bin/env python
#
# Check formatting of Caml files.
# Copy to .git/hooks/pre-commit

import re
import os
import sys
import logging
import subprocess

tabs = re.compile(r'(\t+)')
trail = re.compile(r'([ \t]+)$')

lang_types = ['ml', 'mli', 'mly', 'mll', 'py', 'lint',
              '.hh', '.hpp', '.hxx', '.h++', '.cc', '.cpp',
              '.cxx', '.c++', 'c', 'h']
checkLengthMagic = '__VF_HGHOOK_IGNORE_LONGLINE'


def check_file(filename):
    "return True if the filename can be checked"
    _basename, extension = os.path.splitext(filename)
    return extension.lstrip('.') in lang_types


def linelen(line, tabsize=8):
    tabCnt = line.count('\t')
    if not tabCnt:
        return len(line)

    count = 0
    for c in line:
        if c == '\t':
            count += tabsize - count % tabsize
        else:
            count += 1

    return count


class ValidationStats(object):
    def __init__(self):
        self.toolong = 0
        self.tabs = 0
        self.trailwhite = 0
        self.cret = 0
        self.onMaster = False

    def __nonzero__(self):
        return self.toolong or self.tabs or \
               self.trailwhite or self.cret or \
               self.onMaster


def validate(log, filename, stats, exit_code):
    if not check_file(filename):
        return

    def msg(lineno, line, message):
        log.warn('%s:%d> %s' % (filename, lineno + 1, message))

    def bad():
        if exit_code is not None:
            sys.exit(exit_code)

    try:
        stagedLines = subprocess.check_output(
              'git show ":$(git rev-parse --show-prefix)%s"' % filename,
              shell=True).split('\n')
    except CalledProcessError:
        log.warn('could not open file %s' % filename)
        bad()
        return

    checkLength = True

    for i,line in enumerate(stagedLines):
        # skip line length checks if the magic word is found
        if checkLengthMagic in line:
            checkLength = False

        line = line.rstrip('\n')

        # no carriage returns
        if line.find('\r') != -1:
            stats.cret += 1
            msg(i, line, 'carriage return found')
            bad()

        # lines max out at 90 chars
        llen = linelen(line)
        if checkLength and llen > 90:
            stats.toolong += 1
            msg(i, line, 'line too long (%d chars)' % llen)
            bad()

        # no tabs used to indent
        match = tabs.search(line)
        if match:
            stats.tabs += 1
            msg(i, line, 'using tabs')
            bad()

        # no trailing whitespace
        if trail.search(line):
            stats.trailwhite +=1
            msg(i, line, 'trailing whitespace')
            bad()


def abs_path(repo,f):
    path = os.path.dirname(repo.path)
    return os.path.join(path,f)


def validate_branch(log, errors):
    # The local branch that will push to origin/master (most probably: master)
    masterTrackingBr = subprocess.check_output(
            'git remote show origin|grep \'pushes to master\'|awk \'{print $1}\'',
            shell=True)
    # The checked out branch
    coBranch = subprocess.check_output('git branch|grep \'*\'|awk \'{print $2}\'',
                                       shell=True)
    if coBranch == masterTrackingBr:
        errors.onMaster = True
        log.warn('You are trying to commit to master! Pushing may not be possible.')


def check_format(file):
    errors = ValidationStats()

    validate(logging, file, errors, None)

    return not errors # no errors found

