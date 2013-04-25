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
#import numpy as np #for arange, below

# This script is designed to call the MOEAframework "Analysis" tool
# many many times.  The format of the command is something like:
# java -Xmx1g -classpath MOEAFramework-1.17-Executable.jar 
# org.moeaframework.analysis.sensitivity.Analysis --parameterFile 
# BORG_Params.txt --parameters ./paramValues/BORG_Param_Values.txt 
# --metric 2 --threshold 0.75 --efficiency ./metrics/AllDecAll.average 
#./metrics/LowDecAll.average

# The order of metrics:
#'Hypervolume', ...                      %1
#'Generational Distance', ...            %2
#'Inverse Generational Distance', ...    %3
#'Spacing', ...                          %4
#'Epsilon Indicator', ...                %5
#'Maximum Pareto Front Error'};          %6

LINE_BUFFERED = 1

def main():

    #A bunch of string variables store the various parts of our command.  Outside the loop,
    #we construct the parts of the command that won't change...
    javaArgs = ['-Xmx1g', '-classpath', 'MOEAFramework-1.17-Executable.jar']
    javaCall = ['/usr/bin/java']
    javaProgram = ['org.moeaframework.analysis.sensitivity.Analysis']
    invariantParams = ['--parameterFile', './BORG_Params.txt', '--parameters', './paramValues/BORG_Param_Values.txt', '--efficiency']
      
    #...Including the specific problems we want to calculate
    problems = ['AllDecAll', 'LowDecAll', 'AllDecCostRel', 'LowDecCostRel']
    problemFilenames = ['./metrics/' + problem + '.average' for problem in problems] 
    problemIndices = range(0,4)

    #The following problem hypervolumes are from the "Without Recency" experiment:
    #used to use 0.135184794908381, the hypervolume of the file solutionsFourProblems.noViolation.sorted.txt
    problemHypervolumeValues = ['0.29711526952760375', '0.11603091662956089', '0.485822499851039', '0.5838159649759032'] 

    #Now get ready for the looping.
    #Note: The thresholds array below was created with the numpy library,
    #and the function 'arange'.  On the cluster, numpy is not installed
    #so I just hard-coded the thresholds here.  Anyway, it's probably better
    #because there's no ambiguity about the step size or the end points.
    thresholds = ([0.01,  0.02,  0.03,  0.04,  0.05,  0.06,  0.07,  0.08,
        0.09,  0.1 ,  0.11,  0.12,  0.13,  0.14,  0.15,  0.16,  0.17,
        0.18,  0.19,  0.2 ,  0.21,  0.22,  0.23,  0.24,  0.25,  0.26,
        0.27,  0.28,  0.29,  0.3 ,  0.31,  0.32,  0.33,  0.34,  0.35,
        0.36,  0.37,  0.38,  0.39,  0.4 ,  0.41,  0.42,  0.43,  0.44,
        0.45,  0.46,  0.47,  0.48,  0.49,  0.5 ,  0.51,  0.52,  0.53,
        0.54,  0.55,  0.56,  0.57,  0.58,  0.59,  0.6 ,  0.61,  0.62,
        0.63,  0.64,  0.65,  0.66,  0.67,  0.68,  0.69,  0.7 ,  0.71,
        0.72,  0.73,  0.74,  0.75,  0.76,  0.77,  0.78,  0.79,  0.8 ,
        0.81,  0.82,  0.83,  0.84,  0.85,  0.86,  0.87,  0.88,  0.89,
        0.9 ,  0.91,  0.92,  0.93,  0.94,  0.95,  0.96,  0.97,  0.98,
        0.99,  1.  ])
    percentiles = range(1,101) 
    metricIndices = range(0,5)
    metricNames = ['Hyp', 'GD', 'InGD', 'Spacing', 'EpsInd', 'MaxPFE']

    print "metric indices"
    print metricIndices
    print "problem indices"
    print problemIndices
    
    counter = 0  
    for threshold in thresholds:            
        for metricIndex in metricIndices:
            for problemIndex in problemIndices:

                #For this particular iteration, assign problem and metricName
                problem = problems[problemIndex]
                metricName = metricNames[metricIndex]

                #Turn on for debugging
                #print 'threshold, metricIndex, problemIndex: %f %d %d' % (threshold, metricIndex, problemIndex)
                #print 'therefore problem is %s, metricName is %s' % (problem, metricName)                

                #Construct the arguments specific to this call
                metricArg = ['--metric', str(metricIndex)]
                thresholdArg = ['--threshold', str(threshold)]
                outputArg = ['--output', './analysis/' + problem + '_' + metricName + '_' + str(percentiles[counter]) + '.txt']
                hypervolumeArg = ['--hypervolume', problemHypervolumeValues[problemIndex]]
    
                if metricName == 'Hyp':
                    #command specific to hypervolume must include the reference set hypervolume
                    cmd = ( javaCall + javaArgs + javaProgram + invariantParams + metricArg
                        + thresholdArg + hypervolumeArg + outputArg + [problemFilenames[problemIndex]])
                else:
                    cmd = ( javaCall + javaArgs + javaProgram + invariantParams + metricArg
                        + thresholdArg + outputArg + [problemFilenames[problemIndex]])
                
                #Now that we've constructed the command, we check it for correctness...
                print cmd
                
                #...then fork a process to run it.  Turn this off for debugging purposes.
                child = Popen(cmd, cwd='//work//00868//tg459235//LRGV_2013-03-10_runs-without-recency//parallel-test-256samples', bufsize=LINE_BUFFERED, stdin=PIPE, stdout=PIPE, stderr=PIPE)
                child.wait()

                #WARNING: If the child process above has any sort of error come out of it, you won't know about it unless you
                #process the stdin and stdout from the PIPE.  This isn't hard to do, so you can add it here if you'd like (above
                #the wait())
            
        counter = counter + 1
if __name__ == "__main__":
    main()