""" Check whether a commit message contains the jira ticket in the message """

import re


JIRA_KEYS = 'VFTEST|VFG|VFA|VFS|VFW'


def check_message(message):
    """ Check whether a message contains the Jira-specific header """
    match_str = ".*({0})-[0-9]+".format(JIRA_KEYS)
    match = re.match(match_str, message)
    if not match:
        print "ERROR: Commit message is missing Jira issue number: %s" % message
    return match


def check_messages(messages):
    """ Check whethe a list of messages contains the Jira-specific header """
    errors = 0
    for message in messages:
        if not check_message(message):
            errors += 1
    return errors == 0
