# election-verifier

https://user-images.githubusercontent.com/81968/164185978-953b72b6-3faa-4cad-a93b-879fe191e9b6.mov

`election-verifier` performs universal verification of an election tally in
[Sequent] platform.

The verifications performed are:
1. `recorded-as-cast`: Allows anyone to verify the inclusion of an encrypted
   ballot in the tally.
2. `counted-as-recorded`: Allows anyone to verify that with the given set of
   encrypted ballots, the calculated election results are correct. This
   includes:
   1. The usage of [mixnet] library to verify the `Zero Knowledge Proofs` of:
      1. Key Generation
      1. Ballot Shuffling
      1. Ballot Re-encryption
      1. Joint-decryption of the encrypted ballots
   1. The calculation of election results from the plaintext ballots verified in
     the previous Joint-decryption verification step, using the [tally-pipes]
     and [tally-methods] libraries.

## Usage

You need to be running inside an `Ubuntu 20.04 LTS` operative system on a
`x86_64` machine. You also need to have `openjdk` version 8 installed.
`election-verifier` is currently untested in other system configurations.

If you don't have a tally to verify but you want to test `election-verifier`, you
can find an example of some tallies to verify in `testdata/` directory in this
repository. Note that you need to use a matching software version of
`election-verifier` and this tally to make it work.

In the `testdata/` directory, the file `8.tar` is a valid election tally, and
all the other tallies contain different kind of invalid errors that would make
the verifier fail, showing some red color output and returning a non-zero value
as result.

Finally, to perform recorded-as-cast verification in this testdata, note that a
valid ballot tracker is
`ae38e56fd663c142387ad9f69d710e9afd1e8c28da3f0ba93facdaae65d273e6`.

### Performing `counted-as-recorded` verification

Once you have the `election-verifier` binary and a tally to verify, you can perform
`counted-as-recorded` verification of the tally by running the following 
command:

```bash
chmod +x election-verifier
# Execute by using bash ./election-verifier <path-to-tally.tar>
bash ./election-verifier testdata/8.tar 
```

**Tip:** You can use one of the invalid testdata tallies and see how
`election-verifier` fails on different kind of tally verifications. 

### Performing `recorded-as-cast` verification

You can also verify the inclusion of a ballot tracker with `election-verifier` in
the list of encrypted ballots of the election tally. This is the so-called
`recorded-as-cast` verification. Note that the ballot tracker is just a hash of
the ballot. If the ballot tracker is
`ae38e56fd663c142387ad9f69d710e9afd1e8c28da3f0ba93facdaae65d273e6`, then to
perform this verification on the tally `tally.tar` you would run the
following command:

```bash
chmod +x election-verifier
# Execute by using bash ./election-verifier <path-to-tally.tar> <ballot-tracker>
bash ./election-verifier testdata/8.tar ae38e56fd663c142387ad9f69d710e9afd1e8c28da3f0ba93facdaae65d273e6
```

**Tip:** You can try to make up an invalid ballot-tracker to see that
`election-verifier` does not find it in the tally and fails.

## Building `election-verifier`

### Automatic builds

Compilation and installation of `election-verifier` is already automated in:
- [deployment-tool]: Any new [Sequent] platform deployment automatically compiles
  and ships the `election-verifier` binary with election results, showing voters a
  link to download `election-verifier` in the public election page once the
  election results are published. See [deployment-guide] for instructions on how
  to run `deployment-tool` to deploy the whole system.
- [unit-tests]: `election-verifier` CI pipeline automatically compiles and runs
  `election-verifier` unittests on github. You can directly download the
  `election-verifier` binary used and generated in each run of the 
  [unit-tests Github Actions Workflow] from the summary page of that workflow
  run.

### Manual Build

To manually build yourself the `election-verifier` executable, please follow the
instructions below.

**1. System requirements**

For these instructions, we will be asuming you are using `Ubuntu 20.04 LTS` on a
`x86_64` machine. Deployment has not been tested in any other system
configuration.

**2. Install dependencies**

`election-verifier` uses openjdk `8`, sbt `0.13.18`, and also the `uuencode` 
encoding tools. Let's install them first:

```bash
sudo apt update && \
sudo apt install -y wget sharutils openjdk-8-jdk-headless && \
wget https://scala.jfrog.io/artifactory/debian/sbt-0.13.18.deb && \
sudo dpkg -i sbt-0.13.18.deb && \
sudo update-alternatives --list java && \
sudo update-alternatives --set java /usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java
```

Next, we will be installing the internal dependencies, i.e. dependencies of
`election-verifier` that are also part of [Sequent] platform: [tally-pipes] and
[tally-methods]. Please change the `INTERNAL_GIT_VERSION` variable to the
appropiate version to use in your case.

> :warning: **Note** You need to change the `INTERNAL_GIT_VERSION` you should be
using depending on the version of [Sequent] platform used to run the election you
want to verify. In this example, we're using version `7.0.0` of [Sequent] 
platform.

```bash
export INTERNAL_GIT_VERSION="7.0.0"
git clone https://github.com/sequentech/election-verifier.git
cd election-verifier
git checkout "${INTERNAL_GIT_VERSION}"

git clone https://github.com/sequentech/tally-methods.git
cd tally-methods && git checkout "${INTERNAL_GIT_VERSION}" && cd ..
mv tally-methods/tally_methods .

git clone https://github.com/sequentech/tally-pipes.git
cd tally-pipes && git checkout "${INTERNAL_GIT_VERSION}" && cd ..
mv tally-pipes/ tally-pipes2
mv tally-pipes2/tally_pipes .
mv tally-pipes2/tally-pipes .
```

**3. Building and packaging**

To compile and package the `election-verifier` binary, please run:

```bash
sbt clean proguard:proguard
./package.sh
```

This will generate the `election-verifier` executable in the current working
directory. You can see it's working by running:

```bash
bash ./election-verifier testdata/8.tar
```

**4. Notes on `lib/mixnet.jar`**

This library depends on `mixnet.jar`, which for simplicity is currently
included directly in the git repository. You can build this file from the
[mixnet] repository and copy it back to `lib/mixnet.jar` before executing
the build.

[Sequent]: https://sequentech.io
[mixnet]: https://github.com/sequentech/mixnet
[tally-pipes]: https://github.com/sequentech/tally-pipes
[tally-methods]: https://github.com/sequentech/tally-methods
[deployment-tool]: https://github.com/sequentech/deployment-tool
[unit-tests]: https://github.com/sequentech/election-verifier/blob/master/.github/workflows/unittests.yml
[deployment-guide]: https://sequent.github.io/documentation/docs/deployment/guide/
[unit-tests Github Actions Workflow]: https://github.com/sequentech/election-verifier/actions/workflows/unittests.yml
