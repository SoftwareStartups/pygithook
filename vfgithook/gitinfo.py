""" Commit hook for pylint """
import tempfile
import subprocess

from . import command


def current_commit():
    """Return the current commit (HEAD) revision"""
    if command.execute('git rev-parse --verify HEAD'.split()).status:
        return '4b825dc642cb6eb9a060e54bf8d69288fbee4904'
    else:
        return 'HEAD'


def list_committed_files():
    """ Returns a list of files about to be commited. """
    files = []
    diff_index_cmd = 'git diff-index --cached %s' % current_commit()
    output = subprocess.check_output(
        diff_index_cmd.split()
    )
    for result in output.split('\n'):
        if result != '':
            result = result.split()
            if result[4] in ['A', 'M']:
                files.append(result[5])

    return files


def prev_version_tmp_file(filename):
    """Get the previous version for this file from git into a temp file"""
    cmd = 'git show %s:%s' % (current_commit(), filename)
    result = command.execute(cmd.split())
    if not result.status:
        return None

    tmp_file = tempfile.NamedTemporaryFile(delete=False)
    try:
        tmp_file.write(result.stdout)
    finally:
        tmp_file.close()
    return tmp_file.name
