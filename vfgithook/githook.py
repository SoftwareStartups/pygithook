
"""
This module implements the basic inffrastructure for defining analysis passes
for git hooks. This module provides the base class for githooks as well as an
abstract class which abstract away over the information that can be retrieved
from git for different hooks.

More specifically, we now have a uniform interface for pre-commit and update
hooks to retrieve different version of a file and commit messages, such that
checks can be written for both hooks directly
"""

import os


from . import gitinfo


# pylint: disable=too-few-public-methods

class GitHook(object):
    """
    This is the base class for all git checks. It determines which files
    it will check and implements the itself
    """

    def should_check_file(self, filename):
        """
        Abstract function for determining whether a file should be checked
        """
        raise NotImplementedError

    def check_file(self, changset_info, filename):
        """
        Abstract function for doing the actual check
        """
        raise NotImplementedError


class DisposableFile(object):
    """
    Simple wrapper object for files which may need deletion after consumption
    is done. This base implementation just leaves the file as-is when
    delete is called, the below TemporaryFile is a variant which actually
    does deletion.
    """

    def __init__(self, name):
        self.name = name

    def delete(self):
        """ Dummy implementation of delete """
        self.name = None


class TemporaryFile(DisposableFile):
    """
    This is a subclass of DisposableFile which actually deletes
    a file when delete is called. This can be used to control the
    life-cycle of a file
    """

    def __init__(self, name):
        DisposableFile.__init__(self, name)

    def delete(self):
        """ Delete the file if it wasn't already done """
        if self.name != None:
            os.remove(self.name)
            os.rmdir(os.path.dirname(self.name))
        self.name = None


class ChangeSetInfo(object):
    """ Superclass for getting git data from different git hooks """

    def list_modified_files(self):
        """ All files changed """
        raise NotImplementedError

    def commit_messages(self):
        """ List of commit messages """
        raise NotImplementedError

    def original_content(self, filename):
        """
        Get a handle to the contents of the presented file before the changeset
        """
        raise NotImplementedError

    def current_content(self, filename):
        """
        Get a handle to the contents of the presented file after the changeset
        """
        raise NotImplementedError

    def original_file(self, filename):
        """
        Get a handle to the file of the presented file before the changeset
        """
        raise NotImplementedError

    def current_file(self, filename):
        """
        Get a handle to the file of the presented file after the changeset
        """
        raise NotImplementedError


class PrecommitGitInfo(ChangeSetInfo):
    """
    Git changeset info provider for the pre-commit hook. This typicaly handles
    just one commit and will look at the staged files to determine what files
    are being changed. These functions are actually implemented in gitinfo
    """

    def list_modified_files(self):
        """ Returns a list of files about to be commited. """
        return gitinfo.list_staged_files(gitinfo.current_commit())

    def commit_messages(self):
        """ No commit message provided yet """
        return []

    def original_file(self, filename):
        """ Extract this file from the git history """
        return TemporaryFile(
            gitinfo.revision_tmp_file(gitinfo.current_commit(), filename))

    def current_file(self, filename):
        """ This is the file currently in the tree """
        return TemporaryFile(
            gitinfo.revision_tmp_file("", filename))

    def original_content(self, filename):
        """ Extract the file contents from git """
        return gitinfo.revision_content(gitinfo.current_commit(), filename)

    def current_content(self, filename):
        """ Publish the current contents from the index """
        return gitinfo.revision_content("", filename)


class UpdateGitInfo(ChangeSetInfo):
    """
    Subclass of ChangeSetInfo for retrieving files and commit messages for
    a specific range of commits
    """

    def __init__(self, branch, from_rev, to_rev):
        self.branch = branch
        self.from_rev = from_rev
        self.to_rev = to_rev

    def list_modified_files(self):
        """ This is implemented in gitinfo """
        return gitinfo.list_committed_files(self.from_rev, self.to_rev)

    def commit_messages(self):
        """ Gitinfo knows the details """
        return gitinfo.list_commit_messages(self.from_rev, self.to_rev)

    def original_file(self, filename):
        """ Extract the original from the tree """
        return TemporaryFile(gitinfo.revision_tmp_file(self.from_rev, filename))

    def current_file(self, filename):
        """ Extract the current file from the tree """
        return TemporaryFile(gitinfo.revision_tmp_file(self.to_rev, filename))

    def original_content(self, filename):
        """ Simple relay for gitinfo """
        return gitinfo.revision_content(self.from_rev, filename)

    def current_content(self, filename):
        """ Simple relay for gitinfo """
        return gitinfo.revision_content(self.to_rev, filename)
