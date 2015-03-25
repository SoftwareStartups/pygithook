#!/bin/bash

# This script is supposed to be called from within a git repository and will install the
# vectorfabrics githooks into that repository

# Get the directory of this install script
SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done
DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"

GITDIR=$(git rev-parse --show-toplevel)

# Add the symlinks
ln -sf $DIR/../../../install/bin/pre-commit $GITDIR/.git/hooks/pre-commit
ln -sf $DIR/../../../install/bin/commit-msg $GITDIR/.git/hooks/commit-msg

