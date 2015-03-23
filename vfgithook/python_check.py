""" Check the pylint score between current commit and HEA"""
import decimal
import os
import sys

from . import pylint, gitinfo


def is_python_file(filename):
    """Check if the input file looks like a Python script

    Returns True if the filename ends in ".py" or if the first line
    contains "python" and "#!", returns False otherwise.

    """
    if filename.endswith('.py'):
        return True
    else:
        with open(filename, 'r') as file_handle:
            first_line = file_handle.readline()
        return 'python' in first_line and '#!' in first_line


def pylint_check_files(config, python_files):
    """Check all python_files with pylint"""
    assert len(python_files) > 0

    all_passed = True
    file_count = 1
    for python_file in python_files:
        sys.stdout.write("Running pylint on {} (file {}/{})..\t".format(
            python_file, file_count, len(python_files)))
        sys.stdout.flush()

        passed = pylint_check_file(config, python_file)
        all_passed = all_passed and passed
        file_count += 1

    return all_passed


def pylint_check_file(config, python_file):
    """Check python_file with pylint.
    The check passes if the file is new and has a pylint score >= limit,
    or if the score has not decreased wrt the current version.
    """
    # Allow __init__.py files to be completely empty
    if os.path.basename(python_file) == '__init__.py':
        if os.stat(python_file).st_size == 0:
            return True

    out = pylint.pylint(config, python_file)
    score = pylint.parse_score(out)

    prev_file = gitinfo.prev_version_tmp_file(python_file)
    prev_score = None
    if prev_file:
        try:
            out = pylint.pylint(config, prev_file)
            prev_score = pylint.parse_score(out)
        finally:
            os.remove(prev_file)

    # Verify the score
    if prev_score is None:
        passed = (score >= config.limit)
        sys.stdout.write('{:.2}/10'.format(decimal.Decimal(score)))
    else:
        passed = (score >= prev_score)
        sys.stdout.write('{:.2} -> {:.2}'.format(
            decimal.Decimal(prev_score), decimal.Decimal(score)))

    print '\t%s' % ('PASSED' if passed else 'FAILED')
    return passed


