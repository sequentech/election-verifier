# agora-verifier

`agora-verifier` performs universal verification of an electoral process in
[nVotes] platform.

The verifications performed are:
1. `recorded-as-cast`: Allows anyone to verify the inclusion of an encrypted
   ballot in the tally.
2. `counted-as-recorded`: Allows anyone to verify that with the given set of
   encrypted ballots, the calculated election results are correct. This
   includes:
   - The usage of [vfork] library to verify the `Zero Knowledge Proofs` of:
     - Key Generation
     - Shuffling
     - Joint-decryption of the encrypted ballots
   - The calculation of election results from the plaintext ballots verified in
     the previous Joint-decryption verification step, using the [agora-results]
     and [agora-tally] libraries.

## Usage

You need to be running inside an `Ubuntu 20.04 LTS` operative system on a
`x86_64` machine. You also need to have `openjdk` version 8 installed.
`agora-verifier` is currently untested in other system configurations.

If you don't have a tally to verify but you want to test `agora-verifier`, you
can find an example of some tallies to verify in `testdata/` directory in this
repository. Note that you need to use a matching software version of
`agora-verifier` and this tally to make it work.

In the `testdata/` directory, the tally `12.tar` is a valid election tally, and
all the other tallies contain different kind of invalid errors that would make
the verifier fail, showing some red color output and return a non-zero value.

Finally, to perform recorded-as-cast verification in this testdata, note that a
valid ballot tracker is
`09684d8abd01c2227432bc6302e669fac4e4b3e7251f24c4a9c938683fa44705`.

### Performing `counted-as-recorded` verification

Once you have the `agora-verifier` binary and a tally to verify, you can perform
`counted-as-recorded` verification of the tally by running the following 
command:

```bash
chmod +x agora-verifier
# Execute by using ./agora-verifier <path-to-tally.tar>
./agora-verifier testdata/12.tar 
```

**Tip:** You can use one of the invalid testdata tallies and see how
`agora-verifier` fails on different kind of tally verifications. 

### Performing `recorded-as-cast` verification

You can also verify the inclusion of a ballot tracker with `agora-verifier` in
the list of encrypted ballots of the electoral tally. This is the so-called
`recorded-as-cast` verification. Note that the ballot tracker is just a hash of
the ballot. If the ballot tracker is
`09684d8abd01c2227432bc6302e669fac4e4b3e7251f24c4a9c938683fa44705`, then to
perform this verification on the tally `tally.tar` you would run the
following command:

```bash
chmod +x agora-verifier
# Execute by using ./agora-verifier <path-to-tally.tar> <ballot-tracker>
./agora-verifier testdata/12.tar 09684d8abd01c2227432bc6302e669fac4e4b3e7251f24c4a9c938683fa44705
```

**Tip:** You can try to make up an invalid ballot-tracker to see that
`agora-verifier` does not find it in the tally and fails.

## Building `agora-verifier`

### Automatic builds

Compilation and installation of `agora-verifier` is already automated in:
- [agora-dev-box]: Any new [nVotes] platform deployment automatically compiles
  and ships the `agora-verifier` binary with election results, showing voters a
  link to download `agora-verifier` in the public election page once the
  election results are published. See [deployment-guide] for instructions on how
  to run `agora-dev-box` to deploy the whole system.
- [unit-tests]: `agora-verifier` CI pipeline automatically compiles and runs
  `agora-verifier` unittests on github. You can directly download the
  `agora-verifier` binary used and generated in each run of the 
  [unit-tests Github Actions Workflow] from the summary page of that workflow
  run.

### Manual Build

To manually build yourself the `agora-verifier` executable, please follow the
instructions below.

**1. System requirements**

For these instructions, we will be asuming you are using `Ubuntu 20.04 LTS` on a
`x86_64` machine. Deployment has not been tested in any other system
configuration.

**2. Install dependencies**

`agora-verifier` uses openjdk `8`, sbt `0.13.18`, and also the `uuencode` 
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
`agora-verifier` that are also part of [nVotes] platform: [agora-results] and
[agora-tally]. Please change the `INTERNAL_GIT_VERSION` variable to the
appropiate version to use in your case.

> :warning: **Note** You need to change the `INTERNAL_GIT_VERSION` you should be
using depending on the version of [nVotes] platform used to run the election you
want to verify. In this example, we're using version `5.0.0` of [nVotes] 
platform.

```bash
export INTERNAL_GIT_VERSION="5.0.0"
git clone https://github.com/agoravoting/agora-verifier.git
cd agora-verifier
git checkout "${INTERNAL_GIT_VERSION}"

git clone https://github.com/agoravoting/agora-tally.git
cd agora-tally && git checkout "${INTERNAL_GIT_VERSION}" && cd ..
mv agora-tally/agora_tally .

git clone https://github.com/agoravoting/agora-results.git
cd agora-results && git checkout "${INTERNAL_GIT_VERSION}" && cd ..
mv agora-results/ agora-results2
mv agora-results2/agora_results .
mv agora-results2/agora-results .
```

**3. Building and packaging**

To compile and package the `agora-verifier` binary, please run:

```bash
sbt clean proguard:proguard
./package.sh
```

This will generate the `agora-verifier` executable in the current working
directory. You can see it's working by running:

```bash
./agora-verifier testdata/12.tar
```

[nVotes]: https://nvotes.com
[vfork]: https://github.com/agoravoting/vfork
[agora-results]: https://github.com/agoravoting/agora-results
[agora-tally]: https://github.com/agoravoting/agora-tally
[agora-dev-box]: https://github.com/agoravoting/agora-dev-box
[unit-tests]: https://github.com/agoravoting/agora-verifier/blob/master/.github/workflows/unittests.yml
[deployment-guide]: https://agoravoting.github.io/admin-manual/docs/deployment/guide/
[unit-tests Github Actions Workflow]: https://github.com/agoravoting/agora-verifier/actions/workflows/unittests.yml
