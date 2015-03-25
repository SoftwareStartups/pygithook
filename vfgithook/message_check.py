""" Check whether a commit message contains the VFG message """

import re


def check_message(message):
    """ Check whether a message contains the VF-specific header """
    match = re.match("(VFG|VFA|VFS|VFW)-[0-9]+", message)
    if not match:
        print "ERROR: Commit message is missing Jira issue number: %s" % message
    return match


def check_messages(messages):
    """ Check whethe a list of messages contains the VF-specific header """
    errors = 0
    for message in messages:
        if not check_message(message):
            errors += 1
    return errors == 0
