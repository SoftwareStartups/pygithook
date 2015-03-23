"""Testsuite for vfgithook.python_check"""

from . import util
from vfgithook import githook


def test_basic_style_ok(gitrepo):
    """Test python_check.is_python_file"""

    # Create file 'a'
    file_a = util.write_file(gitrepo, 'a.py', '')
    assert githook.precommit_hook()

    # Add 'a'
    util.cmd(gitrepo, 'git add ' + file_a)
    assert githook.precommit_hook()

    # Commit 'a'
    util.cmd(gitrepo, 'git commit -m msg')
    assert githook.precommit_hook()

def test_basic_style_problem(gitrepo):
    """Test python_check.is_python_file"""

    # Create file 'a'
    file_a = util.write_file(gitrepo, 'a.py', ' ')
    assert githook.precommit_hook()

    # Add 'a'
    util.cmd(gitrepo, 'git add ' + file_a)
    assert not githook.precommit_hook()

    # Commit 'a'
    util.cmd(gitrepo, 'git commit -m msg')
    assert githook.precommit_hook()
