#Copyright (C) 2013 Joseph Kasprzyk, Matthew Woodruff and others.

#This script is free software: you can redistribute it and/or modify
#it under the terms of the GNU Lesser General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This script is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU Lesser General Public License for more details.

#You should have received a copy of the GNU Lesser General Public License
#along with this script.  If not, see <http://www.gnu.org/licenses/>.


import re
import os
import sys
import time
from subprocess import Popen
from subprocess import PIPE

LINE_BUFFERED = 1

def cli():
    if len(sys.argv) != 4:
        sys.stderr.write("Arguments: algorithm, problem, seed\n")
        sys.exit()
    args = {}
    args["algorithm"] = sys.argv[1]
    args["problem"] = sys.argv[2]
    args["seed"] = sys.argv[3] 
    return args
        
def main():

    #Two command line arguments are the problem and the seed.  Each of the lower
    #dimensional problems is being re-evaluated with the AllDecAll objectives.
    args = cli()
    algorithm = args["algorithm"]
    problem = args["problem"]
    seed = args["seed"]
    
    #Input and output filenames.
    inputFilename = './' + algorithm + '/' + problem + '_s' + seed + '.txt'
    outputFilename = './' + algorithm + '/' + problem + '_s' + seed + '.re-evaluated.txt'
    
    #Define the command that you would like to run through the pipe.  This will typically be your
    #executable set up to work with MOEAframework, and associated arguments.  Specifically here
    #we are working with the LRGV problem.
    if problem == "AllDecCostRel":
        newProblem = "AllDecAll"
    elif problem == "LowDecCostRel":
        newProblem = "LowDecAll"
    else:
        print "Error, problem not recognized! You said %s" % problem
    
    cmd = ['./lrgvForMOEAFramework',  '-m', 'std-io', '-c', 'combined', '-b', newProblem]

    #Verify the command
    #print "The command to run is: %s" % cmd

    #Use popen to open a child process.  The standard in, out, and error are sent through a pipe.
    child = Popen(cmd, cwd='//home//joka0958//re-evaluator_2013-04-05//', bufsize=LINE_BUFFERED, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    #When using this python child process, we need to intentionally send and receive all output (i.e. it doesn't
    #automatically do it for us.
    
    #Check whether the current version of the model spits out lines to the console when initializing.
    #When some debug output is turned off, this doesn't occur -- so comment out these lines if appropriate.
    #print "Reading initializer lines."
    for i in range(0,3):
        line = child.stdout.readline()
        if line:
            pass
            #print line
        else:
            raise Exception("Evaluator died!")

    #Now we want to step through an existing Borg output file, which already contains decision variables and objectives.
    #We are going to step through each line, read in the decision variables from the file, and then evaluate those decision
    #variables in our external program.
    inStream = open(inputFilename, 'rb')
    outStream = open(outputFilename, 'w')
    for line in inStream:
        if "#" in line:
            #This "if" statement is helpful if you want to preserve the generation separators and header lines that appeared
            #in the original file.
            #print "Generation separator!"
            outStream.write(line)
        else:
            #Read in all the variables on the line (this is both decisions and objectives)
            allVariables = [float(xx) for xx in re.split("[ ,\t]", line.strip())]

            #Only keep what you want
            if problem == "AllDecCostRel":
                variables = allVariables[0:8]
            elif problem == "LowDecCostRel":
                variables = allVariables[0:3]
            else:
                print "Error! Problem not specified, you said %s" % problem
            
            #We want to send the decision variables, separated by a space, and terminated by a newline character
            decvarsAsString = " ".join(str(x) for x in variables) + "\n"
            #print "Wrapping the decision variables resulted in:"
            #print decvarsAsString
            
            #We send that string to the child process and catch the result.
            #print "Sending to process"
            child.stdin.write(decvarsAsString)
            child.stdin.flush() #you flush, so that the program knows the line was sent

            #Now obtain the program's result
            #print "Result:"
            outputLine = child.stdout.readline()
            #print outputLine

            #Just like processing our input file, we are taking the line from standard out,
            #and converting it into individual floating point numbers.  Of those numbers,
            #we are taking the first six (i.e. we are throwing away the constraint violations)
            outputVariables = [float(xx) for xx in re.split("[ ,\t]", outputLine.strip())]
            objectives = outputVariables[0:6]
            
            #Finally, re-format the output to place in the output file.  We need the decision variables, and then the
            #objective function values.
            outputString = (" ".join(str(x) for x in variables)
                + " "
                + " ".join(str(y) for y in objectives)
                + "\n")
            outStream.write(outputString)

if __name__ == "__main__":
    main()