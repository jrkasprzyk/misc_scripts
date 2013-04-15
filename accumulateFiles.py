#Copyright (C) 2013 Joseph Kasprzyk, Matthew Woodruff, and others.

#This script is free software: you can redistribute it and/or modify
#it under the terms of the GNU Lesser General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This script is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU Lesser General Public License for more details.

#You should have received a copy of the GNU Lesser General Public License
#along with the script.  If not, see <http://www.gnu.org/licenses/>.


from __future__ import with_statement
import os
import sys

def process_contents(contents):
    data = []
    state = "not started"
    for line in contents:
        if state == "not started" and "Problem" in line:
            state = "problem header"
        elif state == "problem header" and "Seed" in line:
            state = "seed"
        elif state == "seed":
            if "#" in line:
                state = "complete"
            elif "//" not in line:
                state = "data"
        elif state == "data":
            if "#" in line:
                state = "complete"
        if state in ["data", "complete"]:
            data.append(line.strip())
        if state == "complete": break
    if state == "complete":
        return data
    else:
        return None

def accumulate_group_directory(dirname, expected):
    """
    dirname: the directory where the files should be found
    expected: a list of filenames in the order that I want them to be
    """
    incomplete = []
    data = {}
    for filename in expected:
        try:
            with open(os.path.join(dirname, filename), 'rb') as fp:
                contents = fp.readlines()
            processed = process_contents(contents)
            if processed:
                data[filename] = processed
            else:
                incomplete.append(filename)
                
        except IOError, OSError:
            incomplete.append(filename)
    
    return {"incomplete": incomplete, "data": data}

def accumulate_seed(basedir, problem, seed, outputdir):
    #The directory name will always be the same (everything is in the same directory)
    dirname = os.path.join(basedir)
    filenumber = 0
    incomplete = []
    
    #Now we need to loop through all experiment files. We will create a list of expected
    #files then call a function to loop through them.

    expected = ["".join([problem, "_Experiment_", str(experiment), "_s", seed, ".txt"]) for experiment in range(256)]
    accumulated = accumulate_group_directory(dirname, expected)
    #print accumulated
    splits = accumulated["incomplete"]

    print "Printing splits:"
    print splits
 
    outputfilename = "".join([problem, "_s", seed, ".txt"])

    fp = open(os.path.join(outputdir, outputfilename), 'wb')

    #for ii in range(3):
    #print "Printing the 0th entry?"
    #print "For file:"
    #print expected[0]
    #print accumulated["data"][expected[0]]
    #print "Printing the 1st entry?"
    #print accumulated["data"][expected[1]]
   
    for ii in range(256):
        fp.write("\n".join(accumulated["data"][expected[ii]]))
        fp.write("\n")

def cli():
    if len(sys.argv) != 3:
        sys.stderr.write("Arguments: problem, seed\n")
        sys.exit()
    args = {}
    args["problem"] = sys.argv[1]
    args["seed"] = sys.argv[2] 
    return args

if __name__ == "__main__":
    args = cli()

    basedir = "/work/00868/tg459235/LRGV_2013-03-10/parallel-test-256samples"
    accumulate_seed(basedir, args["problem"],
                    args["seed"],
                    "/work/00868/tg459235/LRGV_2013-03-10/parallel-test-256samples/sets")
