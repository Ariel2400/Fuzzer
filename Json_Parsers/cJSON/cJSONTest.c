#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/stat.h>
#include "cJSON.h"

int main(int argc, char const *argv[])
{
    struct stat stat_buf;
    int fd;
    fd = open(argv[1], O_RDONLY);
    fstat(fd, &stat_buf);
    int flen=stat_buf.st_size;
    char* json_f_buffer = (char*)malloc(flen);
    FILE *fp = fopen(argv[1], "r");
    fread(json_f_buffer, flen, 1, fp);
    cJSON *json = cJSON_Parse(json_f_buffer);
    char *string = cJSON_Print(json);
    cJSON_Delete(json);
    printf("%s", string);
    return 0;
}
