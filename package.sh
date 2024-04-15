#!/bin/sh

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

rm -r -f dist
mkdir dist
cp -r tally_methods dist
cp -r tally_pipes dist
cp target/scala-2.10/proguard/election-verifier_2.10-10.3.0.jar dist
cp pverify.sh dist
cp vmnc.sh dist
cp verify.py dist
cp tally-pipes dist
tar zcf election-verifier.tar.gz dist --transform s/dist/election-verifier/
cp executable_base.sh election-verifier
uuencode  election-verifier.tar.gz election-verifier.tar.gz >> election-verifier
chmod +x election-verifier
