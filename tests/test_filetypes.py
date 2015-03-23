"""Testsuite for vfgithook.filetypes"""

from . import util
from vfgithook import filetypes


def test_is_python_file(gitrepo):
    """Test filetypes.is_python_file"""

    # Extension
    file_a = util.write_file(gitrepo, 'a.py', '')
    assert filetypes.is_python_file(file_a)

    # Empty
    file_b = util.write_file(gitrepo, 'b', '')
    assert not filetypes.is_python_file(file_b)

    # Shebang
    file_c = util.write_file(gitrepo, 'b', '#!/usr/bin/env python')
    assert filetypes.is_python_file(file_c)
