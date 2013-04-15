/*
Copyright (C) 2013 Joseph Kasprzyk, Matthew Woodruff, David Hadka and others.

This parallel script is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This parallel script is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with the script.  If not, see <http://www.gnu.org/licenses/>.
*/


#include <stdio.h>     /* for sprintf */
#include <stdlib.h>    /* for exit */
#include <mpi.h>       /* for MPI* */
#include <unistd.h>    /* fork and exec */
#include <sys/wait.h>  /* wait() */

int main(int argc, char* argv[]) {
	int rank=-1;
	int id=-1;
	
	/* The child_argv[] contains the main command for the forked process.
		Certain parts of the command will later be replaced below. */
	
	char* child_argv[] = {
		"/usr/bin/java",
		"-Xmx128m",
		"-classpath",
		"MOEAFramework-1.17-Executable.jar",
		"org.moeaframework.analysis.sensitivity.ResultFileEvaluator",
		"-d", "6",
		"-r", "solutionsFourProblems.noViolation.sorted.txt",
		"-i", "",
		"-o", "",
		NULL};

	/*char rankstring[20];*/
	char inputfilestring[255];
	char outputfilestring[255];
	
	char* child_env[] = {NULL};

	/* Initialize MPI, and store the processor rank in the rank variable. */
	MPI_Init(&argc, &argv);
	MPI_Comm_rank(MPI_COMM_WORLD, &rank);
	printf("Hello from rank %d\n", rank);
	if(rank < 50){
	   printf("I, rank %d, am going to do some work.", rank);
	  
	   /* Fork a new process */
	
	   id = fork();
	   if(id == -1){
		   perror("fork");
	   	   exit(EXIT_FAILURE);
	   }
	
	   if(id == 0){/* child */
	
		   /* The child has to prepare to replace the strings appropriately. */
		   sprintf(inputfilestring, "./sets/noDV/AllDecAll_s%d.noDV.txt", rank+1);
		   sprintf(outputfilestring, "./metrics/AllDecAll_s%d.metrics", rank+1);
		   printf("Rank %d input and output strings are: %s, %s\n", rank, inputfilestring, outputfilestring);
		   /* Now replace the strings in the actual command */
		   child_argv[10] = inputfilestring;
		   child_argv[12] = outputfilestring;
		
		   /* Finally, actually call the command */
		   execve("/usr/bin/java", child_argv, child_env);
		   printf("Rank %d just finished his java command.", rank);
	   } else {
	           wait(NULL);
	   }

	} else {
	  printf("I, rank %d, ain't doin nothin.", rank);
	}
	printf("Rank %d is entering the barrier.", rank);
	MPI_Barrier(MPI_COMM_WORLD);
	MPI_Finalize();

	return 0;
}

