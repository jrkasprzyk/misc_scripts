#!/bin/bash

#Copyright (C) 2013 Joseph Kasprzyk and others.

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

PROBLEMS=("AllDecCostRel" "LowDecCostRel")
NSEEDS=50
SEEDS=$(seq 1 ${NSEEDS})

for PROBINDEX in ${!PROBLEMS[*]}
do
    PROBLEM=${PROBLEMS[$PROBINDEX]}
    echo "Problem is ${PROBLEM}"
    
    for SEED in ${SEEDS}
    do
        python reEvaluateMOEAFrameworkModel.py withRecency ${PROBLEM} ${SEED}
    done
done