#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <stdbool.h>
#include <fcntl.h>
#include <stdarg.h>
#include <sys/sysctl.h>
#include <string.h>
#include <sys/wait.h>

#define EXIT_FAILURE	1
#define EXIT_SUCCESS	0

int main(){
	uid_t ruid, euid, suid;
	int fd1 = -1;
	int fd2 = -1;
	int cpid = -1;
	bool privilegedOp = false;
	char *buf1 = "write to unprivileged file1.";
	char *buf2 = "sensitive information in file2.";

	getresuid(&ruid, &euid, &suid);
	/* drop privilege for unprivileged operation */
	/* set effective uid to real uid*/
	seteuid(ruid);

	/* Open, read, close unprivileged file */
	fd1 = open("file_unpriv.txt", O_WRONLY);
	if(fd1<0){
		perror("Reading unprivileged file: ");
		return EXIT_FAILURE;
	}
	seteuid(suid);
	/* Open, read, close unprivileged file */
	fd2 = open("file_priv.txt", O_WRONLY);
	if(fd2<0){
		perror("Reading privileged file: ");
		return EXIT_FAILURE;
	}
	else{
		privilegedOp = true;
	}
	seteuid(ruid);

	cpid = fork();
	if(cpid == 0){
		/* Results of reads above determine value of privilegedOp */
		if(privilegedOp){
			/* Perform privileged operation */
			if(write(fd2, buf2, strlen(buf2))<0){
				perror("Write to privileged file: ");
				return EXIT_FAILURE;
			}
			close(fd2);   
			return EXIT_SUCCESS;     
		}
	}
	write(fd1, buf1, strlen(buf1));
	if(fd1>0) close(fd1);
	wait(NULL);
	return EXIT_SUCCESS;
}
