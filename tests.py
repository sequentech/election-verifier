# -*- coding:utf-8 -*-

# This file is part of tally-pipes.
# Copyright (C) 2017-2021  Sequent Tech Inc <legal@sequentech.io>

# tally-pipes is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License.

# tally-pipes  is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with tally-pipes.  If not, see <http://www.gnu.org/licenses/>.

import unittest
import subprocess

def run_command(command, return_code=None, stdout_contains_text=None, **kwargs):
    '''
    Utility to run a command.
    timeout is in seconds.
    '''
    print("call_cmd: executing command: " + " ".join(command))
    try:
        process = subprocess.run(
            command,
            check=True,
            stdout=subprocess.PIPE,
            **kwargs
        )
        return process
    except subprocess.CalledProcessError as error:
        if return_code == None or error.returncode != return_code:
            raise error
    finally:
        if stdout_contains_text:
            if not process.stdout:
                raise Exception(f"`{stdout_contains_text}` not in stdout")
            process_stdout = process.stdout.decode('utf-8')
            for check_text in stdout_contains_text:
                if check_text not in process_stdout:
                    raise Exception(f"`{check_text}` not in process_stdout")

class TestStringMethods(unittest.TestCase):
    def test_election_8(self):
        '''
        Validates the example proofs for election 8.tar
        '''
        run_command(
            command=["./election-verifier", "./testdata/8.tar"],
        )

    def test_election_invalid_file(self):
        '''
        The file is not found so it fails
        '''
        run_command(
            command=["./election-verifier", "./testdata/non_existing_tarfile.tar"],
            return_code=1
        )

    def test_election_8_wrong_ballots(self):
        '''
        The election proofs fail because the ballots.json file
        is wrong
        '''
        run_command(
            command=["./election-verifier", "./testdata/8_wrong_ballots.tar"],
            return_code=1
        )

    def test_election_8_wrong_proof_of_shuffle(self):
        '''
        The election proofs fail because the proofs of shuffle (file
        0-78b10d61-d525-4aca-998f-cad2f200a1bf/proofs/CCPoSCommitment01.bt)
        have been tampered with.
        '''
        run_command(
            command=[
                "./election-verifier",
                "./testdata/8_wrong_proof_of_shuffle.tar"
            ],
            return_code=1
        )

    def test_election_8_wrong_proof_of_shuffle_existing_ballot(self):
        '''
        The ballot hash locator finds the ballot, because although the 
        proof of shuffle was tampered with, the ballots.json file was not.
        '''
        run_command(
            command=[
                "./election-verifier",
                "./testdata/8_wrong_proof_of_shuffle.tar",
                "ae38e56fd663c142387ad9f69d710e9afd1e8c28da3f0ba93facdaae65d273e6"
            ]
        )

    def test_election_8_wrong_proof_of_shuffle_nonexisting_ballot(self):
        '''
        The ballot hash locator cannot find the ballot. The proof of shuffle was
        tampered with, the ballots.json file was not. The tampering does not
        affect the result in this case because we are only verifying that the
        ballot and its hash is part of the results.
        '''
        run_command(
            command=[
                "./election-verifier",
                "./testdata/8_wrong_proof_of_shuffle.tar",
                "ae38e56fd663c142387ad9f69d710e9afd1e8c28da3f0ba93facdaae65d273e5"
            ],
            return_code=1
        )

    def test_election_8_wrong_results(self):
        '''
        The election proofs fail because the results have been tampered with.
        '''
        run_command(
            command=[
                "./election-verifier",
                "./testdata/8_wrong_results.tar"
            ],
            return_code=1
        )

    def test_election_8_existing_ballot(self):
        '''
        The ballot is located in the ballots.json file.
        '''
        run_command(
            command=[
                "./election-verifier",
                "./testdata/8.tar",
                "ae38e56fd663c142387ad9f69d710e9afd1e8c28da3f0ba93facdaae65d273e6"
            ],
            stdout_contains_text=["weight=1"]
        )

    def test_election_8_existing_ballot_vote_weight(self):
        '''
        The ballot is located in the ballots.json file.
        '''
        run_command(
            command=[
                "./election-verifier",
                "./testdata/8_vote_weight.tar",
                "ae38e56fd663c142387ad9f69d710e9afd1e8c28da3f0ba93facdaae65d273e6"
            ],
            stdout_contains_text=["weight=2"]
        )

    def test_election_8_nonexisting_ballots(self):
        '''
        The ballot is not located in the ballots.json file, because it's not 
        there.
        '''
        run_command(
            command=[
                "./election-verifier",
                "./testdata/8.tar",
                "09684d8abd01c2227432bc6302e669fac4e4b3e7251f24c4a9c938683fa44704"
            ],
            return_code=1
        )
        run_command(
            command=[
                "./election-verifier",
                "./testdata/8.tar",
                "deadbeef"
            ],
            return_code=1
        )
        run_command(
            command=[
                "./election-verifier",
                "./testdata/8.tar",
                "whatever"
            ],
            return_code=1
        )
