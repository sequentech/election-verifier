// This file is part of election-verifier.
// Copyright (C) 2015-2016  Sequent Tech Inc <legal@sequentech.io>

// election-verifier is free software: you can redistribute it and/or modify
// it under the terms of the GNU Lesser General Public License as published by
// the Free Software Foundation, either version 3 of the License.

// election-verifier  is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Lesser General Public License for more details.

// You should have received a copy of the GNU Lesser General Public License
// along with election-verifier.  If not, see <http://www.gnu.org/licenses/>.

name := "election-verifier"

version := "10.4.0"

scalaVersion := "2.10.3"

mainClass := Some("org.sequent.sequent.Verifier")

startYear := Some(2015)

homepage := Some(url("https://github.com/sequentech/election-verifier"))

licenses += ("AGPL-3.0", url("https://www.gnu.org/licenses/agpl-3.0.en.html"))

organizationName := "Sequent Tech Inc"

organizationHomepage := Some(url("https://sequentech.io"))


javaOptions in run += "-Djava.security.egd=file:/dev/./urandom"

fork in run := true

// libraryDependencies += "com.typesafe.play" %% "play-json" % "2.2.1"

// resolvers += "Typesafe repository" at "http://repo.typesafe.com/typesafe/releases/"

proguardSettings

// https://github.com/sbt/sbt-proguard/issues/5

ProguardKeys.proguardVersion in Proguard := "5.0"

ProguardKeys.options in Proguard ++= Seq("-dontnote", "-dontwarn", "-ignorewarnings", "-dontobfuscate")

// ProguardKeys.options in Proguard ++= Seq("-dontnote", "-dontwarn", "-ignorewarnings", "-dontobfuscate", "-dontoptimize")

ProguardKeys.options in Proguard += ProguardOptions.keepMain("org.sequent.sequent.Verifier")

ProguardKeys.options in Proguard += ProguardOptions.keepMain("org.sequent.sequent.Vmnc")

ProguardKeys.options in Proguard += "-keep class mixnet.crypto.RandomDevice { *; }"

ProguardKeys.options in Proguard += "-keep class mixnet.arithm.ModPGroup { *; }"

ProguardKeys.options in Proguard += "-keep class mixnet.crypto.RandomDeviceGen { *; }"

ProguardKeys.options in Proguard += "-keep class * implements com.fasterxml.jackson.databind.cfg.ConfigFeature {*;}"

ProguardKeys.options in Proguard += "-keep class * implements com.fasterxml.jackson.databind.jsontype.TypeIdResolver {*;}"

ProguardKeys.options in Proguard += "-keep class scala.concurrent.forkjoin.ForkJoinPool {*;}"

ProguardKeys.options in Proguard += "-keep class scala.concurrent.forkjoin.ForkJoinWorkerThread {*;}"

ProguardKeys.options in Proguard += "-keep class scala.concurrent.forkjoin.ForkJoinTask {*;}"

ProguardKeys.options in Proguard += "-keep class scala.concurrent.forkjoin.LinkedTransferQueue {*;}"

ProguardKeys.inputFilter in Proguard := { file =>
  file.name match {
    case "mixnet.jar" => Some("!**/safe_prime_table.txt")
    case _ => Some("!META-INF/**")
  }
}
