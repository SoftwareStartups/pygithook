#!/bin/bash

set -x

# Get the directory of this install script
SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done
DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"

GITDIR=$(git rev-parse --show-toplevel)

# Build the hooks
pushd $DIR

make test

make

popd

# Add the symlinks
ln -s $DIR/install/bin/pre-commit $GITDIR/.git/hooks/pre-commit

