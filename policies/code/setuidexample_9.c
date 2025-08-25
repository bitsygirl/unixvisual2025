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

#ifdef __APPLE__
static int mygetresuid(uid_t* ruid, uid_t* euid, uid_t* suid)
{
  int retval, mib[4];
  struct kinfo_proc kp;
  size_t len;

  len = sizeof(kp);

  mib[0] = CTL_KERN;
  mib[1] = KERN_PROC;
  mib[2] = KERN_PROC_PID;
  mib[3] = getpid();

  retval = sysctl(mib, 4, &kp, &len, NULL, 0);
  if (retval == -1)
    return -1;

  if (len <= 0)
    return -1;

  *suid = (kp.kp_eproc.e_pcred.p_svuid);
  *ruid = getuid();
  *euid = geteuid();
  return 0;
}
#endif

int main(){
	uid_t ruid, euid, suid;
	int fd1 = -1;
	int fd2 = -1;
	int cpid = -1;
	bool privilegedOp = false;
	char *buf1 = "write to unprivileged file1.";
	char *buf2 = "sensitive information in file2.";
#ifndef __APPLE__
	getresuid(&ruid, &euid, &suid);
#else
	mygetresuid(&ruid, &euid, &suid);
#endif
	/* drop privilege for unprivileged operation */
	/* set effective uid to real uid*/
	seteuid(ruid);

	/* Open, read, close unprivileged file */
	fd1 = open("file_unprivii.txt", O_WRONLY);
	if(fd1<0){
		perror("Opening unprivileged file for write: ");
		return EXIT_FAILURE;
	}
	seteuid(suid);
	/* Open, read, close unprivileged file */
	fd2 = open("file_priv.txt", O_WRONLY);
	if(fd2<0){
		perror("Opening privileged file for write: ");
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