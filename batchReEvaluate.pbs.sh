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

#PBS -N batchReEvaluate.x
#PBS -l walltime=4:00:00
#PBS -A CEAE00000001
#PBS -l nodes=1:ppn=1
#PBS -j oe

. /curc/tools/utils/dkinit

cd $PBS_O_WORKDIR

#
# Execute the program.
./batchReEvaluate.sh

