/*
Copyright (C) 2013 Joseph Kasprzyk, Matthew Woodruff and others.

This script is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This script is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this script.  If not, see <http://www.gnu.org/licenses/>.
*/

import re
import os
import sys
import time
from subprocess import Popen
from subprocess import PIPE

LINE_BUFFERED = 1
        
def main():

    #Define the command that you would like to run through the pipe.  This will typically be your
    #executable set up to work with MOEAframework, and associated arguments.  Specifically here
    #we are working with the LRGV problem.
    cmd = ['./lrgvForMOEAFramework',  '-m', 'std-io', '-c', 'combined', '-b', 'AllDecAll']

    #Verify the command
    print "The command to run is: %s" % cmd

    #Use popen to open a child process.  The standard in, out, and error are sent through a pipe.
    child = Popen(cmd, cwd='//home//joka0958//re-evaluator_2013-04-05//', bufsize=LINE_BUFFERED, stdin=PIPE, stdout=PIPE, stderr=PIPE)

    #The current version of the model spits out some lines to the console when it initializes them.
    #When using this python child process, we need to intentionally send and receive all output (i.e. it doesn't
    #automatically do it for us.  Here there are 3 initialization lines to catch:
    print "Reading initializer lines."
    for i in range(0,3):
       line = child.stdout.readline()
       if line:
         print line
       else:
         raise Exception("Evaluator died!")

    #Now we want to step through an existing Borg output file, which already contains decision variables and objectives.
    #We are going to step through each line, read in the decision variables from the file, and then evaluate those decision
    #variables in our external program.
    myFilename = "AllDecAllExperimentData.txt"
    fp = open(myFilename, 'rb')
    for line in fp:
        if "#" in line:
            #This "if" statement is helpful if you want to preserve the generation separators and header lines that appeared
            #in the original file.
            print line
        else:
            #Read in all the variables on the line (this is both decisions and objectives)
            allVariables = [float(xx) for xx in re.split("[ ,\t]", line.strip())]

            #Only keep what you want
            variables = allVariables[0:8]

            #We want to send the decision variables, separated by a space, and terminated by a newline character
            decvarsAsString = '%f %f %f %f %f %f %f %f\n' % (variables[0], variables[1], variables[2], variables[3], variables[4], variables[5], variables[6], variables[7])

            #We send that string to the child process and catch the result.
            print "Sending to process"
            child.stdin.write(decvarsAsString)
            child.stdin.flush() #you flush, so that the program knows the line was sent

            #Now obtain the program's result
            print "Result:"
            outputLine = child.stdout.readline()
            print outputLine

            #Since this is in a loop, it will operate for every line in the input file.

if __name__ == "__main__":
    main()