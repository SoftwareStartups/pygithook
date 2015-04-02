vfgithooks
==========

By default the script looks at /home1/local64/vfgithook/config/vfpylintrc, which it passes to pylint.

Installation
------------

make

Usage
------

The commit hook will automatically be called when you are running `git commit`. If you want to skip the tests for a certain commit, use the `-n` flag, `git commit -n`.

### Configuration

Settings are loaded by default from the pylintrc file.

    [vfgithook]
    command=custom_pylint
    params=--rcfile=/path/to/another/pylint.rc
    limit=8.0

_command_ is for the actual command, for instance if pylint is not installed globally, but is in a virtualenv inside the project itself.

_params_ lets you pass custom parameters to pylint

_limit_ is the lowest value which you want to allow for a pylint score.  Any lower than this, and the script will fail and won't commit.

Running tests
-------------

The test suite requires py.test to be installed. Install it with `pip install pytest`, then run the tests by executing the following command (in the project root folder):

    make test

Debugging
---------

Set the following environment variable:

    VFGITHOOK_LOGGING=<installdir>/config/logging.json

Requirements
------------

This commit hook is written in Python and has the following requirements:

- [pylint](http://www.logilab.org/857) (`sudo pip install pylint`)
- Python >2.6 and <3.0
