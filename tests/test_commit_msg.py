"""Testsuite for vfgithook.basic_style"""

from vfgithook import githooks, gitinfo, message_check
from . import util


def test_message_check():
    """ Test whether the message check regexp is functioning """

    assert message_check.check_message("VFTEST-0: Bla")
    assert message_check.check_message("VFTEST-1: Bla")
    assert message_check.check_message("Merged: VFTEST-1: Bla")
    assert not message_check.check_message("Bla!")


def test_message_update_ok(gitrepo):
    """Test whether the update hook will succeed when all is in order"""

    # Create file 'a'
    file_a = util.write_file(gitrepo, 'a.ml', '')
    assert githooks.precommit_hook(util.install_path())

    # Add 'a'
    util.cmd(gitrepo, 'git add ' + file_a)
    assert githooks.precommit_hook(util.install_path())

    # Commit 'a'
    util.cmd(gitrepo, 'git commit -m VFTEST-0')
    assert githooks.precommit_hook(util.install_path())

    start = gitinfo.current_commit()

    # Create file 'b'
    file_b = util.write_file(gitrepo, 'b.ml', '')
    assert githooks.precommit_hook(util.install_path())

    # Add 'b'
    util.cmd(gitrepo, 'git add ' + file_b)
    assert githooks.precommit_hook(util.install_path())

    # Commit 'b'
    util.cmd(gitrepo, 'git commit -m VFTEST-1')
    assert githooks.precommit_hook(util.install_path())

    end = gitinfo.current_commit()

    assert githooks.update_hook("master", start, end, util.install_path())


def test_message_update_fail(gitrepo):
    """ Test whether the update hook will fail when a message is wrong """

    # Create file 'a'
    file_a = util.write_file(gitrepo, 'a.ml', '')
    assert githooks.precommit_hook(util.install_path())

    # Add 'a'
    util.cmd(gitrepo, 'git add ' + file_a)
    assert githooks.precommit_hook(util.install_path())

    # Commit 'a'
    util.cmd(gitrepo, 'git commit -m VFTEST-0')
    assert githooks.precommit_hook(util.install_path())

    start = gitinfo.current_commit_hash()

    # Create file 'b'
    file_b = util.write_file(gitrepo, 'b.ml', '')
    assert githooks.precommit_hook(util.install_path())

    # Add 'b'
    util.cmd(gitrepo, 'git add ' + file_b)
    assert githooks.precommit_hook(util.install_path())

    # Commit 'b'
    util.cmd(gitrepo, 'git commit -m VFTEST-X')
    assert githooks.precommit_hook(util.install_path())

    end = gitinfo.current_commit_hash()

    assert not githooks.update_hook("master", start, end, util.install_path())
