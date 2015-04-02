""" Commit hook for pylint """
import tempfile
import subprocess
import logging

from . import command

# pylint: disable=no-member


NULL_COMMIT = '0000000000000000000000000000000000000000'
START_COMMIT = '4b825dc642cb6eb9a060e54bf8d69288fbee4904'

logger = logging.getLogger(__name__)


def current_commit():
    """Return the current commit (HEAD) revision"""
    if command.execute('git rev-parse --verify HEAD'.split()).status:
        return START_COMMIT
    else:
        return 'HEAD'


def current_commit_hash():
    """ Return the current commit (HEAD) revision's hash """
    return command.execute('git rev-parse HEAD'.split()).stdout.split()[0]


def list_commit_messages(from_rev, to_rev):
    """ Returns a list of commit messages. """
    messages = []
    diff_index_cmd = 'git log --pretty=oneline %s..%s' % (from_rev, to_rev)
    output = subprocess.check_output(
        diff_index_cmd.split()
    )
    for result in output.split('\n'):
        if result != '':
            _, _, message = result.partition(' ')
            messages.append(message)
 
    logger.debug("%s: %s", diff_index_cmd, messages)
    return messages


def list_staged_files(revision):
    """ Returns a list of files about to be commited. """
    files = []
    diff_index_cmd = 'git diff-index --cached %s' % revision
    output = subprocess.check_output(
        diff_index_cmd.split()
    )
    for result in output.split('\n'):
        if result != '':
            result = result.split()
            if result[4] in ['A', 'M']:
                files.append(result[5])

    logger.debug("%s: %s", diff_index_cmd, files)
    return files


def list_committed_files(from_rev, to_rev):
    """ Returns a list of files changed in a range of commits. """
    files = []
    diff_index_cmd = 'git diff --name-only %s %s' % (from_rev, to_rev)
    output = subprocess.check_output(
        diff_index_cmd.split()
    )
    for result in output.split('\n'):
        if result != '':
            files.append(result)

    logger.debug("%s: %s", diff_index_cmd, files)
    return files


def revision_content(revision, filename):
    """Get the previous version for this file from git into a string"""
    cmd = 'git show %s:%s' % (revision, filename)
    result = command.execute(cmd.split())

    logger.debug(cmd)

    if result.status != 0:
        return None

    return result.stdout


def revision_tmp_file(revision, filename):
    """Get the previous version for this file from git into a temp file"""
    result = revision_content(revision, filename)
    if result == None:
        return None

    tmp_file = tempfile.NamedTemporaryFile(delete=False)
    try:
        tmp_file.write(result)
    finally:
        tmp_file.close()
    return tmp_file.name
