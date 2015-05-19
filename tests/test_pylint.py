"""Testsuite for vfgithook.pylint"""

from vfgithook import pylint, githooks

import tests.util as util


def test_parse_score():
    """Test pylint.parse_score"""

    text = 'Your code has been rated at 8.51/10'
    assert pylint.parse_score(text) == 8.51

    text = 'Your code has been rated at 8.51'
    assert pylint.parse_score(text) == 0.0


def test_python_ok(gitrepo):
    """Test whether the python hook will fail when something is wrong"""

    file_a = None

    # Create file 'a'
    file_a = util.write_ok_pyfile(gitrepo, 'a.py')
    assert githooks.precommit_hook()

    # Add 'a'
    util.cmd(gitrepo, 'git add ' + file_a)
    assert githooks.precommit_hook()

    file_a = util.write_file(gitrepo, 'a.py', ' ')
    assert githooks.precommit_hook()

    # Commit 'a'
    util.cmd(gitrepo, 'git commit -m python_ok')
    assert githooks.precommit_hook()


def test_python_problem(gitrepo):
    """Test whether the python hook will fail when something is wrong"""

    # Create file 'a'
    file_a = util.write_file(gitrepo, 'a.py', ' ')
    assert githooks.precommit_hook()

    # Add 'a'
    util.cmd(gitrepo, 'git add ' + file_a)
    assert not githooks.precommit_hook()

    # Commit 'a'
    util.cmd(gitrepo, 'git commit -m python_fail')
    assert githooks.precommit_hook()

def test_python_init(gitrepo):
    """ Test whether the __init__.py file is properly accepted """

    file_ini = util.write_file(gitrepo, '__init__.py', '')
    assert githooks.precommit_hook()

    util.cmd(gitrepo, 'git add ' + file_ini)
    assert githooks.precommit_hook()

    util.cmd(gitrepo, 'git commit -m python_fail')
    assert githooks.precommit_hook()
