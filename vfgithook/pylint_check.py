""" Check the pylint score between current commit and HEA"""
import decimal
import os
import sys

from . import pylint, githook


def _is_python_file(filename):
    """Check if the input file looks like a Python script

    Returns True if the filename ends in ".py" or if the first line
    contains "python" and "#!", returns False otherwise.

    """
    if filename.endswith('.py'):
        return True
    else:
        try:
            with open(filename, 'r') as file_handle:
                first_line = file_handle.readline()
            return 'python' in first_line and '#!' in first_line
        except IOError:
            return False


def _pylint_check_file(config, orig_file, current_file):
    """Check python_file with pylint.
    The check passes if the file is new and has a pylint score >= limit,
    or if the score has not decreased wrt the current version.
    """
    if current_file == None:
        return True

    current_out = pylint.pylint(config, current_file)
    current_score = pylint.parse_score(current_out)

    orig_score = None
    if orig_file:
        orig_out = pylint.pylint(config, orig_file)
        orig_score = pylint.parse_score(orig_out)

    # Verify the score
    if orig_score is None:
        passed = (current_score >= config.limit)
        sys.stdout.write('{:.2f}/10'.format(decimal.Decimal(current_score)))
    else:
        passed = (current_score >= orig_score)
        sys.stdout.write('{:.2f} -> {:.2f}'.format(
            decimal.Decimal(orig_score), decimal.Decimal(current_score)))

    print '\t%s' % ('PASSED' if passed else 'FAILED')
    return passed


class PylintHook(githook.GitHook):
    """
    GitHook subclass for pylint. This hook checks whether we do not regress with
    pylint.
    """
    _default_pylintrc = '/home1/local64/vfgithook/config/vfpylintrc'

    def __init__(self):
        self.config = pylint.config_from_pylintrc(self._default_pylintrc)

    def should_check_file(self, filename):
        return _is_python_file(filename)

    def check_file(self, changeset_info, filename):
        sys.stdout.write("Running pylint on {}..\t".format(filename))
        sys.stdout.flush()
        original_file = changeset_info.original_file(filename)
        current_file = changeset_info.current_file(filename)

        # Allow __init__.py files to be completely empty
        if os.path.basename(filename) == '__init__.py':
            if os.stat(current_file.name).st_size == 0:
                print '\tPASSED'
                return True
        try:
            ret = _pylint_check_file(
                self.config, original_file.name, current_file.name)
        finally:
            original_file.delete()
            current_file.delete()
        return ret

