agora-verifier
==============


agora-verifier performs tally and cryptographic verification of the election process, including key generation, shuffling and joint-decryption, using the verificatum library by Douglas Wikström

Requirements
==============
You need

java (version 7)

    sudo add-apt-repository ppa:webupd8team/java
    sudo apt-get update
    sudo apt-get install oracle-java7-installer
    sudo apt-get install oracle-java7-set-default

if you need to revert to java 8 later

    sudo apt-get install oracle-java8-set-default

sbt (version 0.13.7 used here)

    wget https://dl.bintray.com/sbt/debian/sbt-0.13.7.deb
    dpkg -i sbt-0.13.7.deb

the agora\_tally directory of the agora-tally project

    git clone https://github.com/agoravoting/agora-tally.git
    mv agora-tally/agora_tally .

the agora-results directory of the agora-results directory and the executable python script

    git clone https://github.com/agoravoting/agora-results.git
    mv agora-results/ agora-results2
    mv agora-results2/agora_results .
    mv agora-results2/agora-results .

uuencode

    apt-get install sharutils

Packaging
==============
Run

    sbt clean proguard:proguard
    ./package.sh

this will generate an executable agora-verifier

Running
==============

    ./agora-verifier tally.tar.gz


# License

Copyright (C) 2015 Agora Voting SL and/or its subsidiary(-ies).
Contact: legal@agoravoting.com

This file is part of the agora-verifier module of the Agora Voting project.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.  See the GNU General Public License for more details.

Commercial License Usage
Licensees holding valid commercial Agora Voting project licenses may use this
file in accordance with the commercial license agreement provided with the
Software or, alternatively, in accordance with the terms contained in
a written agreement between you and Agora Voting SL. For licensing terms and
conditions and further information contact us at legal@agoravoting.com .

GNU Affero General Public License Usage
Alternatively, this file may be used under the terms of the GNU Affero General
Public License version 3 as published by the Free Software Foundation and
appearing in the file LICENSE.AGPL3 included in the packaging of this file, or
alternatively found in <http://www.gnu.org/licenses/>.

External libraries
This program distributes libraries from external sources. If you follow the
compilation process you'll download these libraries and their respective
licenses, which are compatible with our licensing.
