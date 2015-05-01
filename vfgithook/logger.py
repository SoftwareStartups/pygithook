"""Setup logging"""

import os
import json
import logging
import logging.config


def setup_logger(default_path='logging.yaml',
                 default_level=logging.INFO,
                 env_key='VFGITHOOK_LOGGING'):
    """Setup logging configuration"""
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as conf_file:
            config = json.load(conf_file)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)
