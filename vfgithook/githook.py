
import os


from . import gitinfo


class GitHook(object):
    """ This is the base class for all git checks. It determines which files it will
    check and implements the itself
    """

    def should_check_file(self, filename):
        raise NotImplementedError

    def check_file(self, changset_info, filename):
        raise NotImplementedError


class DisposableFile(object):

    def __init__(self, name):
        self.name = name

    def delete(self):
        return


class TemporaryFile(DisposableFile):

    def __init__(self, name):
        DisposableFile.__init__(self, name)

    def delete(self):
        if self.name != None:
            os.remove(self.name)


class ChangeSetInfo(object):
    """ Superclass for getting git data from different git hooks """

    # All files changed in this changeset
    def list_modified_files(self):
        raise NotImplementedError

    def commit_messages(self):
        raise NotImplementedError

    # Get a handle to the contents of the presented file before the changeset
    def original_content(self, filename):
        raise NotImplementedError

    # Get a handle to the contents of the presented file after the changeset
    def current_content(self, filename):
        raise NotImplementedError

    # Get a handle to the file of the presented file before the changeset
    def original_file(self, filename):
        raise NotImplementedError

    # Get a handle to the file of the presented file after the changeset
    def current_file(self, filename):
        raise NotImplementedError


class PrecommitGitInfo(ChangeSetInfo):

    def list_modified_files(self):
        """ Returns a list of files about to be commited. """
        return gitinfo.list_staged_files(gitinfo.current_commit())

    def commit_messages(self):
        return []

    def original_file(self, filename):
        return TemporaryFile(
            gitinfo.revision_tmp_file(gitinfo.current_commit(), filename))

    def current_file(self, filename):
        return DisposableFile(filename)

    def original_content(self, filename):
        return gitinfo.revision_content(gitinfo.current_commit(), filename)

    def current_content(self, filename):
        with open(filename) as f:
            ret = f.read()
        return ret


class UpdateGitInfo(ChangeSetInfo):

    def __init__(self, branch, from_rev, to_rev):
        self.branch = branch
        self.from_rev = from_rev
        self.to_rev = to_rev

    def list_modified_files(self):
        return gitinfo.list_committed_files(self.from_rev, self.to_rev)

    def commit_messages(self):
        return gitinfo.list_commit_messages(self.from_rev, self.to_rev)

    def original_file(self, filename):
        return TemporaryFile(gitinfo.revision_tmp_file(self.from_rev, filename))

    def current_file(self, filename):
        return TemporaryFile(gitinfo.revision_tmp_file(self.to_rev, filename))

    def original_content(self, filename):
        return gitinfo.revision_content(self.from_rev, filename)

    def current_content(self, filename):
        return gitinfo.revision_content(self.to_rev, filename)
