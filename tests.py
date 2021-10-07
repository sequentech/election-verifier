# -*- coding:utf-8 -*-

# This file is part of agora-results.
# Copyright (C) 2017-2021  Agora Voting SL <agora@agoravoting.com>

# agora-results is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License.

# agora-results  is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with agora-results.  If not, see <http://www.gnu.org/licenses/>.

import unittest
import subprocess

def run_command(command, return_code=None, **kwargs):
    '''
    Utility to run a command.
    timeout is in seconds.
    '''
    print("call_cmd: executing command: " + " ".join(command))
    try:
        process = subprocess.run(
            command,
            check=True,
            **kwargs
        )
        return process
    except subprocess.CalledProcessError as error:
        if return_code == None or error.returncode != return_code:
            raise error

class TestStringMethods(unittest.TestCase):
    def test_election_12(self):
        run_command(
            command=["./agora-verifier", "./testdata/12.tar"],
        )

    def test_election_invalid_file(self):
        run_command(
            command=["./agora-verifier", "./testdata/non_existing_tarfile.tar"],
            return_code=1
        )

    def test_election_12_existing_ballot(self):
        run_command(
            command=[
                "./agora-verifier",
                "./testdata/12.tar",
                "09684d8abd01c2227432bc6302e669fac4e4b3e7251f24c4a9c938683fa44705"
            ],
        )

    def test_election_12_nonexisting_ballots(self):
        run_command(
            command=[
                "./agora-verifier",
                "./testdata/12.tar",
                "09684d8abd01c2227432bc6302e669fac4e4b3e7251f24c4a9c938683fa44704"
            ],
            return_code=1
        )
        run_command(
            command=[
                "./agora-verifier",
                "./testdata/12.tar",
                "deadbeef"
            ],
            return_code=1
        )
        run_command(
            command=[
                "./agora-verifier",
                "./testdata/12.tar",
                "whatever"
            ],
            return_code=1
        )
