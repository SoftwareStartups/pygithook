""" Commit hook for pylint """
import sys

from . import gitinfo, python_check, pylint


def _committed_python_files():
    """Find Python files"""
    python_files = []
    for filename in gitinfo.list_committed_files():
        try:
            if python_check.is_python_file(filename):
                python_files.append(filename)
        except IOError:
            print 'File not found (probably deleted): {}\t\tSKIPPED'.format(
                filename)
    return python_files


def precommit_hook():
    """Main function doing the checks"""

    python_files = _committed_python_files()
    if len(python_files) == 0:
        sys.exit(0)

    config = pylint.config_from_pylintrc()
    return python_check.pylint_check_files(config, python_files)
