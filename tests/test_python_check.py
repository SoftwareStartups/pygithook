"""Testsuite for vfgithook.python_check"""

from . import util
from vfgithook import python_check


def test_is_python_file(gitrepo):
    """Test python_check.is_python_file"""

    # Extension
    file_a = util.write_file(gitrepo, 'a.py', '')
    assert python_check._is_python_file(file_a)

    # Empty
    file_b = util.write_file(gitrepo, 'b', '')
    assert not python_check._is_python_file(file_b)

    # Shebang
    file_c = util.write_file(gitrepo, 'b', '#!/usr/bin/env python')
    assert python_check._is_python_file(file_c)
