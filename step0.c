#include <unistd.h>
#include <stdio.h>

int main()
{  
  int pid, stat;
  char *in_argv[2] = {"ls", NULL};
  if ((pid = fork()) < 0)
    /*fork() エラー */
    perror("fork");    
  else if (pid == 0) {
    if (execvp(in_argv[0], in_argv) < 0) { // 正常終了ならここで終了
        perror("execvp");
        exit(1); // 異常終了
    }
  } 
  else {
    wait(&stat);
  }
}
