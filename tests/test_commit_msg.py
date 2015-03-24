"""Testsuite for vfgithook.basic_style"""

from . import util
from vfgithook import githooks, gitinfo


def test_message_update_ok(gitrepo):
    """Test whether the update hook will succeed when all is in order"""

    # Create file 'a'
    file_a = util.write_file(gitrepo, 'a.ml', '')
    assert githooks.precommit_hook()

    # Add 'a'
    util.cmd(gitrepo, 'git add ' + file_a)
    assert githooks.precommit_hook()

    # Commit 'a'
    util.cmd(gitrepo, 'git commit -m VFG-0')
    assert githooks.precommit_hook()

    start = gitinfo.current_commit()

    # Create file 'b'
    file_b = util.write_file(gitrepo, 'b.ml', '')
    assert githooks.precommit_hook()

    # Add 'b'
    util.cmd(gitrepo, 'git add ' + file_b)
    assert githooks.precommit_hook()

    # Commit 'b'
    util.cmd(gitrepo, 'git commit -m VFG-1')
    assert githooks.precommit_hook()

    end = gitinfo.current_commit()

    assert githooks.update_hook("master", start, end)


def test_message_update_fail(gitrepo):
    """ Test whether the update hook will fail when a message is wrong """

    # Create file 'a'
    file_a = util.write_file(gitrepo, 'a.ml', '')
    assert githooks.precommit_hook()

    # Add 'a'
    util.cmd(gitrepo, 'git add ' + file_a)
    assert githooks.precommit_hook()

    # Commit 'a'
    util.cmd(gitrepo, 'git commit -m VFG-0')
    assert githooks.precommit_hook()

    start = gitinfo.current_commit_hash()

    # Create file 'b'
    file_b = util.write_file(gitrepo, 'b.ml', '')
    assert githooks.precommit_hook()

    # Add 'b'
    util.cmd(gitrepo, 'git add ' + file_b)
    assert githooks.precommit_hook()

    # Commit 'b'
    util.cmd(gitrepo, 'git commit -m VFG-X')
    assert githooks.precommit_hook()

    end = gitinfo.current_commit_hash()

    assert not githooks.update_hook("master", start, end)

