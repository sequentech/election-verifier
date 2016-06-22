/**
 * This file is part of agora-verifier.
 * Copyright (C) 2015-2016  Agora Voting SL <agora@agoravoting.com>

 * agora-verifier is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as published by
 * the Free Software Foundation, either version 3 of the License.

 * agora-verifier  is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.

 * You should have received a copy of the GNU Affero General Public License
 * along with agora-verifier.  If not, see <http://www.gnu.org/licenses/>.
**/
package org.agoravoting.agora

import scala.util.{Try, Success, Failure}
import java.io.{File, ByteArrayOutputStream, PrintStream}
import vfork.ui.gen.GeneratorTool
import vfork.protocol.mixnet.MixNetElGamalInterface

object Vmnc extends App {

  vmnc(args)

  def vmnc(args: Array[String]) = {
    Try {
      System.setSecurityManager(new NESecurityManager())
      val randomSource = args(0)
      Verifier.ensureRandomSource(randomSource)

      try {
        val prefix = Array("vmnc", randomSource, "")
        val arguments = Array.concat(prefix, args.drop(1))
        println(s"* calling mixnet interface with ${arguments.mkString(" ")}..")
        MixNetElGamalInterface.main(arguments)
      } catch {
        case noexit: NEException => // munch System.exit
        case t: Throwable => throw t
      }

    } match {
      case Success(_) => println("* vmnc call succeeded")
      case Failure(e) => println("* verification FAILED"); e.printStackTrace()
    }
  }
}