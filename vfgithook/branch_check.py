
def validate_branch(log, errors):
    # The local branch that will push to origin/master (most probably: master)
    masterTrackingBr = subprocess.check_output(
            'git remote show origin|grep \'pushes to master\'|awk \'{print $1}\'',
            shell=True)
    # The checked out branch
    coBranch = subprocess.check_output('git branch|grep \'*\'|awk \'{print $2}\'',
                                       shell=True)
    if coBranch == masterTrackingBr:
        errors.onMaster = True
        log.warn('You are trying to commit to master! Pushing may not be possible.')


