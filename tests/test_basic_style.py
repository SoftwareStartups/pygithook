"""Testsuite for vfgithook.basic_style"""

from . import util
from vfgithook import githooks


def test_basic_style_ok(gitrepo):
    """Test whether the basic_style hook will pass when everything is ok"""

    # Create file 'a'
    file_a = util.write_file(gitrepo, 'a.ml', '')
    assert githooks.precommit_hook()

    # Add 'a'
    util.cmd(gitrepo, 'git add ' + file_a)
    assert githooks.precommit_hook()

    # Commit 'a'
    util.cmd(gitrepo, 'git commit -m msg')
    assert githooks.precommit_hook()


def test_basic_style_problem(gitrepo):
    """Test whether the basic_style hook will fail when something is wrong"""

    # Create file 'a'
    file_a = util.write_file(gitrepo, 'a.ml', ' ')
    assert githooks.precommit_hook()

    # Add 'a'
    util.cmd(gitrepo, 'git add ' + file_a)
    assert not githooks.precommit_hook()

    # Commit 'a'
    util.cmd(gitrepo, 'git commit -m msg')
    assert githooks.precommit_hook()
