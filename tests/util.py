"""Test utils"""

import os
import subprocess
import inspect

def write_file(tmp_dir, filename, contents):
    """Write file into temp dir"""
    with open(os.path.join(tmp_dir, filename), 'w') as wfile:
        wfile.write(contents)
    return filename

def install_path():
    """Retrieve the path of the local install"""
    mypath = os.path.dirname( \
            os.path.abspath(inspect.getfile(inspect.currentframe())))
    return os.path.join(mypath, "../install")

def write_ok_pyfile(tmp_dir, filename):
    """Write a proper python file to the given location"""
    mypath = os.path.dirname( \
            os.path.abspath(inspect.getfile(inspect.currentframe())))
    with open(os.path.join(mypath, "ok_py_file.py"), "r") as thisfile:
        return write_file(tmp_dir, filename, thisfile.read())
    return None


def cmd(tmp_dir, args):
    """Execute command in a temp dir"""
    return subprocess.check_output(args.split(), cwd=tmp_dir)
