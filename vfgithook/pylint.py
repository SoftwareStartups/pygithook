""" Call pylint and capture the score """
import os
import sys
import re
import collections
import ConfigParser

from . import command


PylintConfig = collections.namedtuple(
    'PylintConfig',
    'limit, pylint_exe, pylintrc, pylint_params')


def config_from_pylintrc(config):
    """Load hook options from the pylintrc file (if any)"""
    if not os.path.exists(config.pylintrc):
        return config

    conf = ConfigParser.SafeConfigParser()
    conf.read(config.pylintrc)
    if conf.has_option('pre-commit-hook', 'command'):
        config.pylint_exe = conf.get('pre-commit-hook', 'command')
    if conf.has_option('pre-commit-hook', 'params'):
        config.pylint_params += ' ' + conf.get('pre-commit-hook', 'params')
    if conf.has_option('pre-commit-hook', 'limit'):
        config.limit = float(conf.get('pre-commit-hook', 'limit'))
    return config


def pylint(config, python_file):
    """Run pylint on python_file and return the pylint output"""
    try:
        cmd = [config.pylint_exe]

        if config.pylint_params:
            cmd += config.pylint_params.split()
            if '--rcfile' not in config.pylint_params:
                cmd.append('--rcfile={}'.format(config.pylintrc))
        else:
            cmd.append('--rcfile={}'.format(config.pylintrc))

        cmd.append(python_file)
        return command.execute(cmd).stdout
    except OSError:
        print "\nAn error occurred. Is pylint installed?"
        sys.exit(1)


_SCORE_REGEXP = re.compile(
    r'^Your\ code\ has\ been\ rated\ at\ (\-?[0-9\.]+)/10')


def parse_score(pylint_output):
    """Parse the score out of pylint's output as a float

    If the score is not found, return 0.0.

    """
    for line in pylint_output.splitlines():
        match = re.match(_SCORE_REGEXP, line)
        if match:
            return float(match.group(1))
    return 0.0
