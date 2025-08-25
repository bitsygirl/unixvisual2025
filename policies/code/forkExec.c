#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>
#include <fcntl.h>

void showCredentials(){
  printf("\tReal UID: %d\tGID: %d\n",getuid(),getgid());
  printf("\tEff  UID: %d\tGID: %d\n",geteuid(),getegid());
}
int main(int argc, char *argv[]){
  int cpid;
  int status;
  printf ("ForkExec: UNIXvisual socket: %s\n", getenv("FD_TO_UNIXVISUAL"));
  printf("Parent credentials\n");
  showCredentials();
  cpid=fork();
  if (cpid==0){
    printf("Child credentials\n");
    showCredentials();
    seteuid(getuid());
    open("file_priv.txt", O_WRONLY);
    _exit(0);
  }
  wait(&status);
  printf("Parent will exec process to show ids.\n");
  /*  execlp(argv[1],argv[1],(char *)0);*/
  status=  execlp("/Users/manwang/Documents/workspace/UnixVisual/src/policies/code/forkExec2","forkExec2",(char *)0);
  perror("Exec:");
  printf("Exec returned %d\n",status);
  printf("Exec failed\n");
}
