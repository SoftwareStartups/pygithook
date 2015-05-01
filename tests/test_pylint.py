"""Testsuite for vfgithook.pylint"""

from vfgithook import pylint, githooks

import tests.util as util
import inspect


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
    with open(inspect.getfile(inspect.currentframe()), "r") as thisfile:
        file_a = util.write_file(gitrepo, 'a.py', thisfile.read())
    assert githooks.precommit_hook()

    # Add 'a'
    util.cmd(gitrepo, 'git add ' + file_a)
    assert not githooks.precommit_hook()

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
