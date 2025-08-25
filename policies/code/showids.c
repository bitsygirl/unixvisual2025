#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void showCredentials(){
  printf("\tReal UID: %d\tGID: %d\n",getuid(),getgid());
  printf("\tEff  UID: %d\tGID: %d\n",geteuid(),getegid());
}
int main(){
  showCredentials();
}
