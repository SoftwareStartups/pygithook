""" Commit hook for pylint """
import sys

from . import gitinfo, filetypes, pylint_check, pylint


def _committed_python_files():
    """Find Python files"""
    python_files = []
    for filename in gitinfo.list_committed_files():
        try:
            if filetypes.is_python_file(filename):
                python_files.append(filename)
        except IOError:
            print 'File not found (probably deleted): {}\t\tSKIPPED'.format(
                filename)
    return python_files


def precommit_python(
        limit, pylint_exe='pylint', pylintrc='.pylintrc', pylint_params=None):
    """Main function doing the checks"""

    python_files = _committed_python_files()
    if len(python_files) == 0:
        sys.exit(0)

    config = pylint.PylintConfig(limit, pylint_exe, pylintrc, pylint_params)
    config = pylint.config_from_pylintrc(config)
    return pylint_check.pylint_check_files(config, python_files)
