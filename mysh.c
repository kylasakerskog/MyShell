#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#define max_char 256
#define max_words 100

int revises_input_cmd(char input[max_char], int len, char revised_input[max_char]);
int split_cmd(char revised_input[max_char], int len, char *in_argv[max_char]);

int main(){
  char input_cmd[max_char];
  char revised_input[max_char];
  char *in_argv[max_words];
  int len = 0;
  //Step 2
  int i = 0; //文字数におけるループ時の条件
  int words = 0; //単語数におけるループ時の条件
  int pid = 0;
  int stat = 0;
  
  for(;;){
    words = 0;
    fprintf(stderr, "mysh$ ");
    //文字数がmax_charを超えた時にエラー
    if(fgets(input_cmd, max_char, stdin) == NULL){
      fprintf(stderr, "fgets error");
      exit(1);
    }
    //fprintf(stderr, "%s",input_cmd); //step1 output
    len = strnlen(input_cmd, max_char);
    //fprintf(stderr, "%d",len);
    if(input_cmd[len-1] == '\n'){
      input_cmd[len-1] = '\0';
      //input_cmd[len] = 0;
    }
    //'exit'を入力した時の対処
    if(strncmp(input_cmd, "exit", max_char) == 0){
      exit(3); 
    }
    
    //cd, chdir

    len = revises_input_cmd(input_cmd, len, revised_input);
    //printf("%s\n",revised_input);
    words = split_cmd(revised_input, len, in_argv);

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

    /* 出力
    for(i=0;i<words;i++){
      if(in_argv[i] != '\0'){
        fprintf(stderr, "in_argv[%d]:%s;\n", i, in_argv[i]);
      }
      free(in_argv[i]); //malloc解放
    }
    */
  }
}

int split_cmd(char revised_input[max_char], int len, char *in_argv[max_char]){
  //単語数を出力
  int words = 0;
  int word_length = 0; //1単語の長さ
  int word_start = 0; //単語分割後の格納時のスタート地点
  int i = 0;
  for(i=0;i<len;i++){
    if(revised_input[i] == ' ' || revised_input[i] == '\0'){
      word_length = i - word_start;
      if(word_length==0){
        break;
      }
      //mallocの確保不足のエラー対処
      if ((in_argv[words] = malloc(max_char)) == NULL){
        fprintf(stderr, "malloc error");
        exit(2);
      }
      strncpy(in_argv[words], &revised_input[word_start], word_length);
      *(in_argv[words]+word_length)='\0';
      words++;
      word_start = (i + 1);
    }
  }
  //単語数が多かった時のエラー処理
  //文字数ですでにエラー処理をしているため，配列格納後に単語数でエラー処理すれば良いと考えた，
  if(words > max_words){
    fprintf(stderr, "word excession error");
    exit(4);
  }
  return words;
}

int revises_input_cmd(char input[max_char], int len, char revised_input[max_char]){
  int i = 0;
  int j = 0;
  for(i=0;i<len;i++){
    if(input[i] == ' '){
      if(i == 0){
          //スペースが最初に入った場合無視
      }
      else if(input[i-1] == ' '){
        //スペースが連続した場合1個に統一
      }
      else{
        revised_input[j] = input[i];
        j++;
      }
    }
    else{
      revised_input[j]=input[i];
      j++;
    }
  }  
  //revised_input[j] = 0;
  return j;
}
