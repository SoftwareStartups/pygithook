""" Commit hook for pylint """
import sys
import logging

from . import githook, pylint_check, basic_style, pylint, gitinfo, message_check, branch_check


hooks = [pylint_check.PylintHook(), basic_style.BasicStyleHook()]


def run_hooks(changset_info):
    errors = 0
    for filename in changset_info.list_modified_files():
        for hook in hooks:
            if hook.should_check_file(filename) \
               and not hook.check_file(changset_info, filename):
                errors += 1
    if errors != 0:
        print "VF POLICY ERROR: please fix the above errors and commit again. (%d errors)" % errors

    return errors == 0


def precommit_hook():
    branch_check.validate_branch()
    return run_hooks(githook.PrecommitGitInfo())


def update_hook(branch, from_rev, to_rev):

    if from_rev == gitinfo.null_commit:
        from_rev = gitinfo.start_commit

    changset_info = githook.UpdateGitInfo(branch, from_rev, to_rev)

    hooks_ok = run_hooks(changset_info)
    messages_ok = message_check.check_messages(changset_info.commit_messages())

    return hooks_ok and messages_ok


def message_hook(message_file):
    with open(message_file) as msg:
        return message_check.check_message(msg.read())
    return False

