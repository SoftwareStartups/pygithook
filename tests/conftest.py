"""Pytest fixtures"""

import os
import shutil
import tempfile
import pytest

from . import util


@pytest.fixture
def gitrepo(request):
    """Create a git repo in a temp dir, remove upon teardown"""
    # Create temporary directory
    tmp_dir = tempfile.mkdtemp(prefix='pylint_hook_test_')

    # Set current working directory to the temporary directory for
    # all the commands run in the test
    os.chdir(tmp_dir)

    # Initialize temporary git repository
    util.cmd(tmp_dir, 'git init')

    request.addfinalizer(lambda: shutil.rmtree(tmp_dir))
    return tmp_dir
