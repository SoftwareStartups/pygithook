vfgithooks
==========

By default the script looks in the root directory of your project for a .pylintrc file, which it passes to pylint.  It also looks for a [pre-commit-hook] section for options of it's own.

Installation
------------

	make

Usage
------

The commit hook will automatically be called when you are running `git commit`. If you want to skip the tests for a certain commit, use the `-n` flag, `git commit -n`.

### Configuration

Settings are loaded by default from the .pylintrc file in the root of your repo.

    [pre-commit-hook]
    command=custom_pylint
    params=--rcfile=/path/to/another/pylint.rc
    limit=8.0

_command_ is for the actual command, for instance if pylint is not installed globally, but is in a virtualenv inside the project itself.

_params_ lets you pass custom parameters to pylint

_limit_ is the lowest value which you want to allow for a pylint score.  Any lower than this, and the script will fail and won't commit.

Any of these can be bypassed directly in the pre-commit hook itself.  You can also set a different default place to look for the pylintrc file.

Running tests
-------------

The test suite requires py.test to be installed. Install it with `pip install pytest`, then run the tests by executing the following command (in the project root folder):

    make test

Requirements
------------

This commit hook is written in Python and has the following requirements:

- [pylint](http://www.logilab.org/857) (`sudo pip install pylint`)
- Python >2.6 and <3.0
