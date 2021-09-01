#!/bin/sh

# This file is part of agora-verifier.
# Copyright (C) 2015-2016  Agora Voting SL <agora@agoravoting.com>

# agora-verifier is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License.

# agora-verifier  is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with agora-verifier.  If not, see <http://www.gnu.org/licenses/>.

if [ "$#" -ne 2 ] || ! [ -d "$2" ]; then
  echo "Usage: $0 <random_source> <tally_dir>" >&2
  exit 1
fi

command -v java >/dev/null 2>&1 || { echo >&2 "* I require java but it's not installed.  Aborting."; exit 1; }

java -Djava.security.egd=file:/dev/./urandom -classpath agora-verifier_2.10-4.0.0-beta.1.jar org.agoravoting.agora.Verifier $1 $2
exit $?
