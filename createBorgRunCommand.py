# Copyright (C) 2015 Joseph Kasprzyk

# This script is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This script is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with the script.  If not, see <http://www.gnu.org/licenses/>.
#
# Program description:
# A set of several classes that enable the user to construct a simple Borg running command and submit it
# using a system subprocess command.  Requires OrderedDict from collections, and subprocess.

from collections import OrderedDict
import subprocess

class Objective(object):
    def __init__(self, name, epsilon):
        self.name = name
        self.epsilon = epsilon


class Decision(object):
    def __init__(self, name, lower, upper):
        self.name = name
        self.lower = lower
        self.upper = upper


def construct_system_command(borgExecutableName, resultFileName, seed, nfe, objectives, decisions, problemExecutableName, problemArgs):
    # This function constructs the borg system command.
    # Example:
    # ./borg.exe -f cost-ee-strength-cover_highmiles_coarse_sl25_balanced_miles.txt
    # -s 1 -v 7 -o 4 -e 0.5,2,50,0.005 -n 100000 -l 550.0,0.25,1.0,55.0,0.0,0.5,1.0
    # -u 700.0,0.75,6.0,75.0,15.0,3.49,30.0 python mix_for_borg.py

    # The first component is the borg executable name
    systemCommand = borgExecutableName

    # The next several components can be in any order, but we will prescribe the order

    # The result filename
    systemCommand = systemCommand + " -f " + resultFileName

    # The seed
    systemCommand = systemCommand + " -s %d" % seed

    # The run duration
    systemCommand = systemCommand + " -n %d " % nfe

    # Constraints
    systemCommand = systemCommand + " -c %d " % numConstraints	
	
    # Objectives (two parts)

    # Objectives Part 1: The number of objectives
    systemCommand = systemCommand + " -o %d " % int(len(objectives))

    # Objectives Part 2: The epsilons
    systemCommand = systemCommand + " -e "

    for key in objectives:
        systemCommand = systemCommand + "%.6f," % objectives[key].epsilon

    systemCommand = systemCommand[:-1].strip() #get rid of the last comma

    # The decisions (three parts)

    # Decisions Part 1: The number of decisions
    systemCommand = systemCommand + " -v %d " % int(len(decisions))

    # Decisions Part 1: The lower bounds
    systemCommand = systemCommand + " -l "

    for key in decisions:
        systemCommand = systemCommand + "%.6f," % decisions[key].lower

    systemCommand = systemCommand[:-1].strip() #get rid of the last comma

    # Decisions Part 2: The upper bounds
    systemCommand = systemCommand + " -u "

    for key in decisions:
        systemCommand = systemCommand + "%.6f," % decisions[key].upper

    systemCommand = systemCommand[:-1].strip() #get rid of the last comma

    # Now the python part

    systemCommand = systemCommand + " -- " + problemExecutableName + " " + problemArgs

    return systemCommand

if __name__ == "__main__":

    # Some code to test the construct_system_command function

    borgExecutableName = "./borgExec"

    seed = 1
    nfe = 10000
    problemExecutableName = "./myExecutable.exe"
    problemArgs = ""

    # List of objectives
    # Create an OrderedDict of instances of the objective objects. The ordered dict
    # is important because we want to make sure that we loop through these
    # objectives in a specified order.  Arguments to the
    # objectives constructor are name, epsilon.
    objectives = OrderedDict()
    objectives["cost"] = Objective("cost", 0.1)
    objectives["performance"] = Objective("performance", 0.001)

    # List of decisions
    # Similar to above.  An ordered dict of decision objects.
    # Arguments to a decision constructor are name, lower bound, upper bound
    decisions = OrderedDict()
    #decisions["control1"] = Decision("control1", 10, 100)
    #decisions["option"] = Decision("option", 0, 4)

    # Assume you had a set of objectives that are just generic objectives with the same
    # epsilons you wanted to loop through. It would look something like this:
    numDecisions = 100
    # Below, define a starting index for the tags of the objectives.  For example, you could start your tags at 0, or 1
    # or whatever else you'd like
    startingIndex = 1

    for i in range(startingIndex, numDecisions+startingIndex):
        myKey = "dec%d" % i
        myLower = 0.0
        myUpper = 0.1
        decisions[myKey] = Decision(myKey, myLower, myUpper)

    numConstraints = 2

    resultFileName = "my_results.txt"

    systemCommand = construct_system_command(borgExecutableName, resultFileName, seed, nfe, objectives, decisions,
                                             problemExecutableName, problemArgs)

    print "The system command is %s" % systemCommand

    # A simple flag to turn the actual RUNNING of the algorithm on or off
    runAlgorithm = 0
    if runAlgorithm:
        print "Running the MOEA"
        subprocess.check_output(systemCommand)
    else:
        print "MOEA will not run because the runAlgorithm variable is set to 0"
