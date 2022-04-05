#!/bin/bash

# portable realpath
#
# https://github.com/AsymLabs/realpath-lib
#
# This  function is Copyright (C) Applied Numerics Ltd 2013-2014, Great
# Britain, under the brand name AsymLabs (TM) and is provided to the community
# under the MIT license. Although we have not yet encountered any issues, there
# is no warranty of any type given so you must use it at your own risk.
function get_realpath {
  # failure : file does not exist
  [[ ! -f "$1" ]] && return 1

  # do symlinks
  [[ -n "$no_symlinks" ]] && local pwdp='pwd -P' || local pwdp='pwd'

  # echo result
  echo "$( cd "$( echo "${1%/*}" )" 2>/dev/null; $pwdp )"/"${1##*/}"

  # success
  return 0
}

# check if tally was correctly provided
if [[ ! -f "$1" ]]
then
  echo "Please specify the path of the tally:"
  echo "$0 <tally.tar>"
  exit 1
fi

# absolute path to the election-verifier binary
binary_path=$(get_realpath $0)

# create a temporal directory, and be sure to remove it on termination
temp_path=$(mktemp -d)
echo "created temporal directory: $temp_path"
trap "echo 'Removing temporal directory: $temp_path'; rm -rf $temp_path" SIGINT SIGTERM SIGQUIT

# absolute path to the tally
tally=$(get_realpath $1)

# extract the binary
cd $temp_path
uudecode -o /dev/stdout $binary_path | tar zxf -

cd $temp_path/election-verifier/

# if ballot locator is provided, then use it, else launch verify script without
# ballot locator
if [[ ! -z "$2" ]]
then
  ballot_locator=$2
  /usr/bin/env python3 verify.py $tally $ballot_locator
  export EXIT_VALUE=$?
else
  /usr/bin/env python3 verify.py $tally
  export EXIT_VALUE=$?
fi

# remove temporal files normally
echo "removing temporal directory: $temp_path"
rm -rf $temp_path

exit $EXIT_VALUE

