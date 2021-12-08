# agora-verifier

agora-verifier performs the tally and cryptographic verification of the election
process, including key generation, shuffling and joint-decryption, using the
[vfork] library. It also verifies the calculation of the election results using
the [agora-results] and [agora-tally] libraries.

## Usage

### Verifying a tally

Once you have the `agora-verifier` binary and a tally to verify, it's simple
to do. You would need to just run:

```bash
./agora-verifier tally.tar.gz
```

> :warning: **Note**  You need to be running inside `Ubuntu 20.04 LTS` on a
`x86_64` machine. `agora-verifier` is currently untested in other
configurations.

### Verifying the inclusion of a ballot tracker in a tally

You can also verify the inclusion of a ballot tracker with `agora-verifier`.
Note that the ballot tracker is just a hash of the ballot. If the ballot tracker
is `9cfd2cedc12d7cf9ec7dcdae041ad6faaf0d52931c886b615b3075dc7f013d70`, then to
perform this verification on the tally `tally.tar.gz` you would do:

```bash
./agora-verifier tally.tar.gz 9cfd2cedc12d7cf9ec7dcdae041ad6faaf0d52931c886b615b3075dc7f013d70
```

## Build

### Automatic builds

Please note that compilation and installation is already automated in:
- [agora-dev-box]: Any new [nVotes] platform deployment automatically compiles
  and ships the `agora-verifier` binary with election results. See
  [deployment-guide] for instructions on how to run `agora-dev-box` to deploy
  the whole system.
- [unit-tests]: automatically compiles and runs `agora-verifier` unittests on
  github commits and pushes.

For most up-to-date instrucions on how to install, please review the
[unit-tests] Github Actions workflow.

### Manual Build

To manually build yourself the `agora-verifier`, please follow the instructions
below. 

**1. System requirements**

For these instructions, we will be asuming you are using `Ubuntu 20.04 LTS` on 
a `x86_64` machine. Deployment has not been tested in any other configuration.

**2. Install dependencies**

`agora-verifier` uses openjdk `8` and sbt `0.13.18`, and also the `uuencode` 
encoding tools. Let's install them:

```bash
sudo apt update
sudo apt install -y wget sharutils openjdk-8-jdk-headless
wget https://scala.jfrog.io/artifactory/debian/sbt-0.13.18.deb
sudo dpkg -i sbt-0.13.18.deb
sudo update-alternatives --list java
sudo update-alternatives --set java /usr/lib/jvm/adoptopenjdk-8-hotspot-amd64/bin/java
```

Now we are installing the internal dependencies, i.e. dependencies of
`agora-verifier` that are also part of [nVotes] platform: [agora-results] and
[agora-tally]. Please change the `INTERNAL_GIT_VERSION` variable to the
appropiate version to use in your case.

> :warning: **Note** that you need to change the `INTERNAL_GIT_VERSION` you
should be using depending on the version of [nVotes] platform used to run the
election you want to verify.

export INTERNAL_GIT_VERSION="5.0.0"
git clone https://github.com/agoravoting/agora-tally.git
cd agora-tally && git checkout "${INTERNAL_GIT_VERSION}" && cd ..
mv agora-tally/agora_tally .

git clone https://github.com/agoravoting/agora-results.git
cd agora-results && git checkout "${INTERNAL_GIT_VERSION}" && cd ..
mv agora-results/ agora-results2
mv agora-results2/agora_results .
mv agora-results2/agora-results .

**3. Building and packaging**

To build the Scala code and package all the code together, please run:

```bash
sbt clean proguard:proguard
./package.sh
```

This will generate the `agora-verifier` executable.

[nVotes]: https://nvotes.com
[vfork]: https://github.com/agoravoting/vfork
[agora-results]: https://github.com/agoravoting/agora-results
[agora-tally]: https://github.com/agoravoting/agora-tally
[agora-dev-box]: https://github.com/agoravoting/agora-dev-box
[unit-tests]: https://github.com/agoravoting/agora-verifier/blob/master/.github/workflows/unittests.yml
[deployment-guide]: https://agoravoting.github.io/admin-manual/docs/deployment/guide/
