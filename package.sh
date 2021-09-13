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

rm -r -f dist
mkdir dist
cp -r agora_tally dist
cp -r agora_results dist
cp target/scala-2.10/proguard/agora-verifier_2.10-master.jar dist
cp pverify.sh dist
cp vmnc.sh dist
cp verify.py dist
cp agora-results dist
tar zcf agora-verifier.tar.gz dist --transform s/dist/agora-verifier/
cp executable_base.sh agora-verifier
uuencode  agora-verifier.tar.gz agora-verifier.tar.gz >> agora-verifier
chmod +x agora-verifier
