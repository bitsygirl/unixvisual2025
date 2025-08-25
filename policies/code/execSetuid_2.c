#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <stdbool.h>
#include <fcntl.h>
#include <stdarg.h>
#include <sys/sysctl.h>
#include <string.h>

#define EXIT_FAILURE	1
#define EXIT_SUCCESS	0

int main(){
	/* drop privilege for unprivileged operation */
	/* set effective uid to real uid*/
	seteuid(0);
	execlp("/Users/manwang/Documents/workspace/UnixVisual/src/policies/code/forkExec2","forkExec2",(char *)0);
	perror("execlp: "); 
	return EXIT_SUCCESS;
}