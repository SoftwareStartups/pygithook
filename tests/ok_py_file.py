""" File used as a proper python file in the test infrastructure """

import os
import subprocess
import inspect

def lorem(tmpdir, filename, contents):
    """Write file into temp dir"""
    with open(os.path.join(tmpdir, filename), 'w') as wfile:
        wfile.write(contents)
    return filename


def ipsum(tmpdir, filename):
    """Write a proper python file to the given location"""
    mypath = os.path.dirname( \
            os.path.abspath(inspect.getfile(inspect.currentframe())))
    with open(os.path.join(mypath, "ok_py_file.py"), "r") as thisfile:
        return lorem(tmpdir, filename, thisfile.read())
    return None


def dolor(tmpdir, args):
    """Execute command in a temp dir"""
    return subprocess.check_output(args.split(), cwd=tmpdir)
