"""Testsuite for vfgithook.pylint_check"""

from vfgithook import pylint_check

from . import util


# pylint: disable=protected-access


def test_is_python_file(gitrepo):
    """Test pylint_check.is_python_file"""

    # Extension
    file_a = util.write_file(gitrepo, 'a.py', '')
    assert pylint_check._is_python_file(file_a)

    # Empty
    file_b = util.write_file(gitrepo, 'b', '')
    assert not pylint_check._is_python_file(file_b)

    # Shebang
    file_c = util.write_file(gitrepo, 'b', '#!/usr/bin/env python')
    assert pylint_check._is_python_file(file_c)
