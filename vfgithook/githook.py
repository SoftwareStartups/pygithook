""" Commit hook for pylint """
import sys
import logging

from . import gitinfo, python_check, basic_style, pylint


class GitHook(object):
    """ This is the base class for all git checks. It determines which files it will
    check and implements the itself
    """

    def should_check_file(self, file):
        raise NotImplementedError

    def check_file(self, file):
        raise NotImplementedError


class PylintHook(GitHook):
    """ GitHook subclass for pylint. This hook checks whether we do not regress with
    pylint. """

    def __init__(self):
        self.config = pylint.config_from_pylintrc()

    def should_check_file(self, file):
        return python_check.is_python_file(file)

    def check_file(self, file):
        return python_check.pylint_check_file(self.config, file)


class BasicStyleHook(GitHook):
    """ Basic hooks to check basic coding style metrics """

    def should_check_file(self, file):
        return basic_style.check_file(file)

    def check_file(self, file):
        return basic_style.check_format(file)

hooks = [PylintHook(), BasicStyleHook()]

def precommit_hook():
    logging.basicConfig(format='%(message)s', level=logging.INFO)
    errors = 0
    for filename in gitinfo.list_committed_files():
        for hook in hooks:
            try:
                if hook.should_check_file(filename) \
                   and not hook.check_file(filename):
                    errors += 1
            except IOError:
                print 'File not found (probably deleted): {}\t\tSKIPPED'.format(
                    filename)
    if errors != 0:
        logging.error("VF POLICY ERROR: please fix the above errors and commit again. (%d errors)" % errors)

    return errors == 0
