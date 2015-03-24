
import re

from . import githook


def check_message(message):
    match = re.match("(VFG|VFA|VFS|VFW)-[0-9]+", message)
    if not match:
        print "ERROR: Commit message is missing Jira issue number: %s" % message
    return match


def check_messages(messages):
    errors = 0
    for message in messages:
        if not check_message(message):
            errors += 1
    return errors == 0
