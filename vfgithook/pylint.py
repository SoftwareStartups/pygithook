""" Call pylint and capture the score """
import os
import sys
import re
import collections
import logging
import ConfigParser

from . import command


PylintConfig = collections.namedtuple(
    'PylintConfig',
    'limit, pylint_exe, pylintrc, pylint_params')

LOGGER = logging.getLogger(__name__)


def config_from_pylintrc(pylintrc='.pylintrc'):
    """Load hook options from the pylintrc file (if any)"""
    config = PylintConfig(10.0, 'pylint', pylintrc, '')

    if os.path.exists(pylintrc):
        conf = ConfigParser.SafeConfigParser()
        conf.read(pylintrc)
        section = 'vfgithook'
        if conf.has_option(section, 'command'):
            config.pylint_exe = conf.get(section, 'command')
        if conf.has_option(section, 'params'):
            config.pylint_params += ' ' + conf.get(section, 'params')
        if conf.has_option(section, 'limit'):
            config.limit = float(conf.get(section, 'limit'))

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

        cmd += ['--reports=y', '--persistent=n', python_file]
        res = command.execute(cmd)
        LOGGER.debug(cmd)
        return res.stdout
    except OSError:
        print "\nAn error occurred. Is pylint installed?"
        sys.exit(1)


_SCORE_REGEXP = re.compile(
    r'^Your\ code\ has\ been\ rated\ at\ (\-?[0-9\.]+)/10')


def parse_score(pylint_output):
    """
    Parse the score out of pylint's output as a float
    If the score is not found, return 0.0.
    """
    for line in pylint_output.splitlines():
        match = re.match(_SCORE_REGEXP, line)
        if match:
            score = float(match.group(1))
            LOGGER.debug("%s, score=%.2f", line, score)
            return score
    return 0.0
