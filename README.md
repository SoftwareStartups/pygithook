pygithook
=========

Extendable python library and scripts to create git hooks. Performs a number of actions on committed files:
- check for line length, tabs vs spaces
- check pylint. It only fails the commit if pylint on this version is worse than the previous version, or below a preset minimum.
- check commit messages for a Jira issue ID

Developed by Vector Fabrics, hence the "VF" names...

Customization
-------------

Jira project keys (to check for in commit messages) are hardcoded in `vfgithook/message_check.py`
Max line length is hardcoded in `vfgithook/basic_style.py`

Installation
------------

To install run:

    make

Then run `install/install.sh` from within the git repo you want to enable the hooks for. This will install the hooks as symlinks to the install dir. This allows you to update the githooks repo and update all hooks without having to go through all your git repos again.

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

- Python >2.6 and <3.0
- [pylint](http://www.logilab.org/857) (`pip install pylint`)
