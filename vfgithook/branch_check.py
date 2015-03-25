""" Check whether the current commit is done on the master branch """

import subprocess

def validate_branch():
    """ Issue a waring when a commit is being done on the master branch """
    # The local branch that will push to origin/master (most probably: master)
    master_tracking_br = subprocess.check_output(
       'git remote show origin|grep \'pushes to master\'|awk \'{print $1}\'',
       shell=True)
    # The checked out branch
    co_branch = subprocess.check_output(
        'git branch|grep \'*\'|awk \'{print $2}\'', shell=True)
    if co_branch == master_tracking_br:
        print 'You are trying to commit to master! Pushing may not be possible.'


