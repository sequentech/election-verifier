#!/usr/bin/env python3

# This file is part of agora-verifier.
# Copyright (C) 2015-2021  Agora Voting SL <agora@agoravoting.com>

# agora-verifier is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License.

# agora-verifier  is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with agora-verifier.  If not, see <http://www.gnu.org/licenses/>.

from agora_tally import tally as agora_tally
import sys
import os
import signal
import hashlib
import shutil
import subprocess
import json
import tarfile
import traceback
from tempfile import mkdtemp

hash_f = hashlib.sha256

class TextColor:
    Header = '\033[95m'
    OkBlue = '\033[94m'
    OkGreen = '\033[92m'
    Warn = '\033[93m'
    Fail = '\033[91m'
    EndColor = '\033[0m'
    Bold = '\033[1m'
    Underline = '\033[4m'

def print_color(color, text):
    print(color + text + TextColor.EndColor)


def print_info(text):
    print_color(TextColor.OkBlue, text)

def print_success(text):
    print_color(TextColor.OkGreen, text)

def print_fail(text):
    print_color(TextColor.Fail, text)

def print_warn(text):
    print_color(TextColor.Warn, text)

def __pretty_print_base(results, filter_names):
    '''
    percent_base:
      "total" total of the votes, the default
      "valid options" votes to options
    '''
    def get_percentage(num, base):
      if base == 0:
          return 0
      else:
        return num*100.0/base

    counts = results['questions']
    for question, i in zip(counts, range(len(counts))):
        if question['tally_type'] not in filter_names or question.get('no-tally', False):
            continue
        print_info("\n\nQ: %s\n" % question['title'])

        blank_votes = question['totals']['blank_votes']
        null_votes = question['totals']['null_votes']
        valid_votes = question['totals']['valid_votes']

        total_votes = blank_votes + null_votes + valid_votes

        percent_base = question['answer_total_votes_percentage']
        if percent_base == "over-total-votes":
          base_num = total_votes
        elif percent_base == "over-total-valid-votes":
          base_num = question['totals']['valid_votes']


        print_info("Total votes: %d" % total_votes)
        print_info("\nOptions (percentages over %s, %d winners):" % (percent_base, question['num_winners']))

        answers = [answer for answer in question['answers']
            if answer['winner_position'] is not None]
        answers.sort(key=lambda answer: answer['winner_position'])

        for i, answer in zip(range(len(answers)), answers):
            print_info("%d. %s (%0.2f votes)" % (
                i + 1, answer['text'],
                answer['total_count']))
    print("")

def compare_hashes(message, hash1, hash2):
    if (hash1 != hash2):
        print_fail("* %s FAILED: %s != %s" % (
            message, hash1, hash2
        ))
        sys.exit(1)

def verify_pok_plaintext(pk, proof, ciphertext):
    '''
    verifies the proof of knowledge of the plaintext, given encrypted data and
    the public key

    Format: * "ballot" must be a dictionary with keys "alpha", "beta",
        "commitment", "challenge", "response", and values must be integers. *
        "pk" must be a dictonary with keys "g", "p", and values must be
        integers.
    
    http://courses.csail.mit.edu/6.897/spring04/L19.pdf
    2.1 Proving Knowledge of Plaintext
    '''
    pk_p = pk['p']
    pk_g = pk['g']
    commitment = int(proof['commitment'])
    response = int(proof['response'])
    challenge =  int(proof['challenge'])
    alpha = int(ciphertext['alpha'])

    # verify the challenge is valid
    hash = hash_f()
    hash.update(("%d/%d" % (alpha, commitment)).encode('utf-8'))
    challenge_calculated = int(hash.hexdigest(), 16)
    assert challenge_calculated == challenge

    first_part = pow(pk_g, response, pk_p)
    second_part = (commitment * pow(alpha, challenge, pk_p)) % pk_p

    # check 
    # g^response == 
    #   commitment * (g^t) ^ challenge == 
    #   commitment * (alpha) ^ challenge
    assert first_part == second_part

def verify_votes_pok(pubkeys, dir_path, tally, hash):
    num_invalid_votes = 0
    linenum = 0
    ciphertexts_path = os.path.join(dir_path, 'ciphertexts_json')

    with open(ciphertexts_path, mode='r') as votes_file:
        num_questions = len(tally['questions'])
        # we will write the ciphertexts for each question in here
        outvotes_files = []
        list_dir = os.listdir(dir_path)
        list_dir.sort()
        for question_dir in list_dir:
            question_path = os.path.join(dir_path, question_dir)
            if not os.path.isdir(question_path):
                continue

            outvotes_path = os.path.join(question_path, 'ciphertexts_json')
            outvotes_files.append(open(outvotes_path, 'w'))

        for i in range(num_questions):
            # (DISABLED FEATURE) if it's a duplicated question, do not verify it
            # TODO: verify it's a duplicated question
            #if "source_question_index" in tally['questions'][i]:
                #continue
            pubkeys[i]['g'] = int(pubkeys[i]['g'])
            pubkeys[i]['p'] = int(pubkeys[i]['p'])

        found = False
        for line in votes_file:
            vote = json.loads(line)
            linenum += 1

            if linenum % 1000 == 0 and not hash:
                print_success(
                    "* Verified %d votes (%d invalid).." % (
                        linenum, num_invalid_votes
                    )
                )
            
            if (
                hash and 
                not found and
                hash_f(line[:-1].encode('utf-8')).hexdigest() == hash
            ):
                found = True
                print_success(
                    "* Hash of the vote was successfully found: %s" % hash
                )

            is_invalid = False
            if not hash or (hash is not None and found):
                try:
                    for i in range(num_questions):
                        # (DISABLED FEATURE) if it's a duplicated question, do not verify it
                        # TODO: verify it's a duplicated question
                        #if "source_question_index" in tally['questions'][i]:
                            #continue
                        verify_pok_plaintext(
                            pubkeys[i],
                            vote['proofs'][i],
                            vote['choices'][i]
                        )
                    if hash is not None and found:
                        print_success("* Verified POK of the found ballot")
                        return 0, found

                except SystemExit as e:
                    break
                    raise e
                except:
                    is_invalid = True
                    num_invalid_votes += 1

            if is_invalid:
                continue

            choice_num = 0
            for f in outvotes_files:
                f.write(
                    json.dumps(
                        vote['choices'][choice_num],
                        ensure_ascii=False,
                        sort_keys=True,
                        separators=(",", ":")
                    )
                )
                f.write("\n")
                choice_num += 1

        for f in outvotes_files:
          f.close()
    
    if not hash:
        print_success(
            "* ..finished. Verified %d votes (%d invalid)" % (
                linenum,
                num_invalid_votes
            )
        )
    return num_invalid_votes, found

if __name__ == "__main__":

    v = sys.version_info
    if v.major < 3 or v.minor < 3:
        print_fail(
            "python3 must be at least 3.3, but it's %d.%d" % (
                v.major,
                v.minor
            )
        )
        sys.exit(1)

    RANDOM_SOURCE=".rnd"

    if len(sys.argv) < 2:
        print_fail('verify.py <tally file> [vote hash]')
        sys.exit(1)

    # untar the plaintexts
    dir_path = mkdtemp("tally")
    tally_gz = tarfile.open(sys.argv[1], mode="r")

    # second argument is the hash of the vote
    hash = None
    if len(sys.argv) > 2:
        hash = sys.argv[2]
        print_info(
            "* Vote hash %s given, we will search the corresponding ballot.." % hash
        )

    def remove_tmp_dir():
        if os.path.exists(dir_path):
            print("\n* removing extract directory: " + dir_path, end="..")
            shutil.rmtree(dir_path)
            print("DONE")

    def sig_handler(__signum, __frame):
        print_fail("* caught an exit signal")
        remove_tmp_dir()
        exit(1)

    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)

    tally_gz.extractall(path=dir_path)
    print("* extracted to " + dir_path)

    # raw tallies
    tallies = [
        file_name 
        for file_name in os.listdir(dir_path)
        if (
            os.path.isfile(os.path.join(dir_path, file_name)) and
            file_name.endswith('tar.gz')
        )
    ]
    tallies.sort(key=lambda x: int(x.split('.')[0]))

    # first extract tallies in order to run agora-results
    for current_tally in tallies:
        number = int(current_tally.split('.')[0])
        tally_raw_gz = tarfile.open(
            os.path.join(dir_path, current_tally), 
            mode="r:gz"
        )
        dir_raw_path = os.path.join(dir_path, 'tally-raw-%d' % number)
        os.mkdir(dir_raw_path)
        tally_raw_gz.extractall(path=dir_raw_path)
        print("* extracted raw tally to " + dir_raw_path)

    # results hash
    tallyfile = os.path.join(dir_path, 'results.json')
    tallyfile_s = open(tallyfile).read()
    tallyfile_json = json.loads(tallyfile_s)
    if "results_dirname" in tallyfile_json:
        if type(tallyfile_json["results_dirname"]) != str:
            print_fail("* tally verification FAILED: invalid results_dirname")
            remove_tmp_dir()
            sys.exit(1)
        del tallyfile_json["results_dirname"]
        tallyfile_s = json.dumps(
            tallyfile_json,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ": "),
            indent=4
        )+"\n"
    hashone = hash_f(tallyfile_s.encode('utf-8')).hexdigest()

    # results hash two
    results_config_path = os.path.join(dir_path, 'config.json')
    tally_list = [os.path.join(dir_path, tally) for tally in tallies]
    command = ['./agora-results', '-t']
    command.extend(tally_list)
    command.extend(['-c', results_config_path, '-s', '-o', 'json'])
    print_info('* running %s ' % command)
    ret = subprocess.check_output(command)
    tallyfile_json2 = json.loads(ret.decode(encoding='UTF-8'))
    hashtwo = hash_f(ret).hexdigest()

    compare_hashes("tally verification", hashone, hashtwo)

    print_success("* results hash verification OK")

    hash_found = False

    for current_tally in tallies:
        number = int(current_tally.split('.')[0])
        dir_raw_path = os.path.join(dir_path, 'tally-raw-%d' % number)
        print('* processing %s' % dir_raw_path)

        print_info("# Results ##########################################")
        __pretty_print_base(tallyfile_json,
            filter_names=[
                "plurality-at-large",
                "borda-nauru",
                "desborda",
                "desborda2",
                "desborda3",
                "borda",
                "pairwise-beta"
            ]
        )

        pubkeys_path = os.path.join(dir_raw_path, "pubkeys_json")
        pubkeys = json.loads(open(pubkeys_path).read())

        print_info("* verifying proofs of knowledge of the plaintexts...")
        try:
            num_encrypted_invalid_votes, found = verify_votes_pok(
                pubkeys,
                dir_raw_path,
                tallyfile_json,
                hash
            )
            hash_found = hash_found or found
            print_success(
                "* proofs of knowledge of plaintexts OK (%d invalid)" % num_encrypted_invalid_votes
            )

            if hash:
                # if we got a hash and we found it, we are done
                if hash_found:
                    print_success("* ALL verifications succeeded")
                    remove_tmp_dir()
                    sys.exit(0)
                # in any case, do not verify the proofs of shuffle or decryption
                # if the hash was provided
                else:
                    continue

            print_info(
                "* Verifying proofs of shuffle and decryption by running " +
                "'./pverify.sh " + str(RANDOM_SOURCE) + " " + dir_raw_path + "'"
            )
            pverify_ret = subprocess.call(
                ['./pverify.sh', RANDOM_SOURCE, dir_raw_path]
            )
            
            if (pverify_ret != 0):
                print_fail("* mixing and decryption verification FAILED")
                raise Exception()
            print_success(
                "* Verification of tally proofs of shuffle and " +
                "decryption OK"
            )

            # check if plaintexts_json is generated correctly from the already
            # verified plaintexts raw proofs
            i = 0
            list_dir = os.listdir(dir_raw_path)
            list_dir.sort()
            for question_dir in list_dir:
                question_path = os.path.join(dir_raw_path, question_dir)
                if not os.path.isdir(question_path):
                    continue

                print_info("* processing question_dir " + question_dir)

                if not question_dir.startswith("%d-" % i):
                    print_fail("* invalid question dirname FAILED")
                    raise Exception()

                if i >= len(tallyfile_json2["questions"]):
                    print_fail("* invalid question dirname FAILED")
                    raise Exception()

                cwd = os.getcwd()
                vmnc = os.path.join(os.getcwd(), "vmnc.sh")

                # verify plaintexts raw conversion
                print_info(
                    "* running '" + vmnc + " " + str(RANDOM_SOURCE) + 
                    " -plain -outi json proofs/PlaintextElements.bt " +
                    "plaintexts_json2'"
                )
                subprocess.call([
                    vmnc,
                    RANDOM_SOURCE, 
                    "-plain",
                    "-outi",
                    "json",
                    "proofs/PlaintextElements.bt",
                    "plaintexts_json2"],
                    cwd=question_path
                )

                path1 = os.path.join(
                    dir_raw_path,
                    question_dir,
                    "plaintexts_json"
                )
                path2 = os.path.join(
                    dir_raw_path,
                    question_dir,
                    "plaintexts_json2"
                )

                path1_s = open(path1).read()
                path2_s = open(path2).read()
                hash1 = hash_f(path1_s.encode('utf-8')).hexdigest()
                hash2 = hash_f(path2_s.encode('utf-8')).hexdigest()
                if (hash1 != hash2):
                    print_fail("* plaintexts_json verification FAILED")
                    raise Exception()
                print_success("* plaintexts_json verification OK")

                # verify ciphertexts raw conversion
                print_info(
                    "* running '" + 
                    vmnc + 
                    " " + 
                    str(RANDOM_SOURCE) + 
                    " -ciphs -ini json ciphertexts_json ciphertexts_raw'"
                )
                subprocess.call(
                    [
                        vmnc,
                        RANDOM_SOURCE,
                        "-ciphs",
                        "-ini",
                        "json",
                        "ciphertexts_json",
                        "ciphertexts_raw"
                    ],
                    cwd=question_path
                )

                path1 = os.path.join(
                    dir_raw_path,
                    question_dir,
                    "ciphertexts_raw"
                )
                path2 = os.path.join(
                    dir_raw_path,
                    question_dir,
                    "proofs",
                    "CiphertextList00.bt"
                )

                path1_s = open(path1, "rb").read()
                path2_s = open(path2, "rb").read()
                hash1 = hash_f(path1_s).hexdigest()
                hash2 = hash_f(path2_s).hexdigest()
                if (hash1 != hash2):
                    print_fail("* ciphertexts_json verification FAILED")
                    raise Exception()
                print_success("* ciphertexts_json verification OK")

                i += 1
        except Exception as error:
            print_fail(
                "* tally verification FAILED due to an error processing it:"
            )
            traceback.print_exc()
            remove_tmp_dir()
            sys.exit(1)
    
    remove_tmp_dir()

    if hash:
        if not hash_found:
            print_fail("* ERROR: vote hash %s NOT FOUND" % hash)
            traceback.print_exc()
            sys.exit(1)
        else:
            print_success("* ballot hash verification OK")

    print_success("* ALL verifications succeeded")
