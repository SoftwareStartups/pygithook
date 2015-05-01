"""Testsuite for vfgithook.gitinfo"""

from . import util
from vfgithook import gitinfo


def test_current_commit(gitrepo):
    """Test gitinfo.current_commit"""

    # Test empty tree
    empty_hash = '4b825dc642cb6eb9a060e54bf8d69288fbee4904'
    assert gitinfo.current_commit() == empty_hash

    # Test after commit
    util.cmd(gitrepo, 'git commit --allow-empty -m msg')
    assert gitinfo.current_commit() == 'HEAD'


def test_list_staged_files(gitrepo):
    """Test gitinfo.list_staged_files"""

    # Test empty tree
    assert len(gitinfo.list_staged_files(gitinfo.current_commit())) == 0

    # Create file 'a'
    file_a = util.write_file(gitrepo, 'a', 'foo')
    assert len(gitinfo.list_staged_files(gitinfo.current_commit())) == 0

    # Add 'a'
    util.cmd(gitrepo, 'git add ' + file_a)
    assert gitinfo.list_staged_files(gitinfo.current_commit()) == [file_a]

    # Change 'a' to 'b' and check what is staged
    file_a = util.write_file(gitrepo, 'a', 'bar')
    assert gitinfo.revision_content("", file_a) == "foo"

    # Commit 'a'
    util.cmd(gitrepo, 'git commit -m msg')
    assert len(gitinfo.list_staged_files(gitinfo.current_commit())) == 0

    # Edit 'a'
    util.write_file(gitrepo, 'a', 'bar')
    assert len(gitinfo.list_staged_files(gitinfo.current_commit())) == 0

    # Add 'a'
    util.cmd(gitrepo, 'git add ' + file_a)
    assert gitinfo.list_staged_files(gitinfo.current_commit()) == [file_a]

