""" Commit hook for pylint """

from . import githook, pylint_check, basic_style, \
    gitinfo, message_check, branch_check


def hooks(installdir):
    """Functio producing the hooks to run """
    return [pylint_check.PylintHook(installdir), basic_style.BasicStyleHook()]


def run_hooks(changset_info, installdir):
    """
    This function iterates over all changed files and runs
    the defined hooks on each of them, returning whether any issues were
    found.
    """
    errors = 0
    for filename in changset_info.list_modified_files():
        for hook in hooks(installdir):
            if hook.should_check_file(filename) \
               and not hook.check_file(changset_info, filename):
                errors += 1
    if errors != 0:
        print "VF POLICY ERROR: please fix the above \
                errors and commit again. (%d errors)" % errors

    return errors == 0


def precommit_hook(installdir):
    """ Function to be called from the pre-commit hook """
    branch_check.validate_branch()
    return run_hooks(githook.PrecommitGitInfo(), installdir)


def update_hook(branch, from_rev, to_rev, installdir):
    """ Function to be called from the update hook """

    if from_rev == gitinfo.NULL_COMMIT:
        from_rev = gitinfo.START_COMMIT

    changset_info = githook.UpdateGitInfo(branch, from_rev, to_rev)

    hooks_ok = run_hooks(changset_info, installdir)
    messages_ok = message_check.check_messages(changset_info.commit_messages())

    return hooks_ok and messages_ok


def message_hook(message_file, _dirnotused):
    """ Function to be called from the commit-msg hook """
    with open(message_file) as msg:
        return message_check.check_message(msg.read())
    return False

