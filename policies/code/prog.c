
#include <unistd.h>
#include <fcntl.h>
#include <string.h>
#include <stdio.h>
#include <errno.h>
#include <stdlib.h>

void report(uid_t real)
{
  printf("Real UID: %d Effect UID: %d\n", real, geteuid());
}

int main()
{
  int fd = open("myfile", O_WRONLY | O_CREAT, S_IRUSR | S_IWUSR);

  const char* txt;
  ssize_t sz;

  txt = "stufftowrite\n";
  sz = write(fd, txt, strlen(txt));
  close(fd);

  fd = open("myfile", O_RDONLY);
  char buffer[100];
  sz = read(fd, buffer, sizeof(buffer));
  close(fd);

  uid_t ruid, euid;
  ruid = getuid();
  euid = geteuid();
  seteuid(ruid);

  int id = fork();
  if(id == 0){
    char* eargv[4];
    char buffs[4][30];
    eargv[0] = buffs[0];
    eargv[1] = buffs[1];
    strcpy(eargv[0], "assert");
    strcpy(eargv[1], "0");
    // strcpy(eargv[0], "/bin/ls");
    // strcpy(eargv[1], "./");
    eargv[2] = NULL;
    fd = open("myfile", O_RDONLY);
    sz = read(fd, buffer, sizeof(buffer));
    close(fd);
    execvp(eargv[0], eargv);
  }

  // seteuid(suid);
  fd = open("myfile1", O_WRONLY);
  txt = "2stufftowrite\n";
  sz = write(fd, txt, strlen(txt));
  close(fd);
  sleep(2);
  return 0;
}

