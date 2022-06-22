#include "./include/json.h"
#include <stdlib.h>
#include <stdio.h>

int main(int argc, char* argv[]){
    printf(argv[1]);
    fflush(stdout);
    FILE *fp = fopen(argv[1], "r");
    printf("opened\n");
    fflush(stdout);
    fseek(fp, 0, SEEK_END);
    printf("here1\n");
    fflush(stdout);
    int size = ftell(fp);
    printf("%d\n", size);
    fflush(stdout);
    fseek(fp, 0, SEEK_SET);
    char *json_buf = (char *)malloc(size);
    fread(json_buf, 1, size, fp);
    printf(json_buf);
    fflush(stdout);
    fflush(stdout);
    fclose(fp);
    printf("\n PARSE \n");
    json_t *j = json_parse(json_buf);
    return 0;
}