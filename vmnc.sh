#!/bin/bash

# This file is part of election-verifier.
# Copyright (C) 2015-2016  Sequent Tech Inc <legal@sequentech.io>

# election-verifier is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License.

# election-verifier  is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with election-verifier.  If not, see <http://www.gnu.org/licenses/>.

command -v java >/dev/null 2>&1 || { echo >&2 "* I require java but it's not installed.  Aborting."; exit 1; }

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

java -Djava.security.egd=file:/dev/./urandom -classpath $DIR/election-verifier_2.10-6.0.0-beta.1.jar org.sequent.sequent.Vmnc "$@"
