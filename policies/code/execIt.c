#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/wait.h>

uid_t ruid, euid, suid;
gid_t rgid, egid, sgid;


void showuids()
{
  euid=geteuid();
  ruid=getuid();
  printf("Process %d: ruid <%d>  euid <%d>\n",getpid(),ruid,euid);
}
void showgids()
{
  egid=getegid();
  rgid=getgid();
  
  printf("Process %d: rgid <%d>  egid <%d> \n",getpid(),rgid,egid);
}

extern char **environ;

int main(int argc, char *argv[], char *envp[]){

  int i;
  int status;
  int cpid;
  uid_t savedEuid;

  showuids();
  showgids();
  savedEuid=geteuid();

  /*  printf("setenv returned <%d>\n",status);
  for (i=0;environ[i]!=(char *)0;i++){printf("environ[%d]=<%s>\n",i,environ[i]);}
  */
  /* Child turns down id before exec */
  cpid=fork();
  if (cpid==0){
      printf("Child turning down the privilege--------\n");
      setuid(getuid());
      setgid(getgid());
      execlp("/usr/bin/id","id",(char *)0);
      exit(1);
  }
  wait(&status);
  showuids();
  showgids();

  /* Parent sets EUID to RUID temporarily */
  printf("Parent sets EUID to RUID temporarily.\n");
  seteuid(getuid());
  showuids();

  printf("Parent sets EUID back to saved temporarily.\n");
  seteuid(savedEuid);
  showuids();

  /* Child can get back */
  printf("Parent sets EUID to RUID temporarily.\n");
  seteuid(getuid());
  showuids();

  cpid=fork();
  if (cpid==0){
      printf("Child tries to turn privilege up\n");
      seteuid(savedEuid);
      showuids();
      exit(0);
  }
  /* Child cannot get back */
  printf("Parent sets all ids to RUID.\n");
  setuid(getuid());
  showuids();

  cpid=fork();
  if (cpid==0){
      printf("Child tries to turn privilege up\n");
      seteuid(savedEuid);
      showuids();
      exit(0);
  }
  
}
  
