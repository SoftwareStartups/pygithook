"""Test utils"""

import os
import subprocess


def write_file(tmp_dir, filename, contents):
    """Write file into temp dir"""
    with open(os.path.join(tmp_dir, filename), 'w') as wfile:
        wfile.write(contents)
    return filename


def cmd(tmp_dir, args):
    """Execute command in a temp dir"""
    return subprocess.check_output(args.split(), cwd=tmp_dir)
