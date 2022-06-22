#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/stat.h>
#include "cJSON.h"

int main(int argc, char const *argv[])
{
    char *json_f_buffer = argv[1];
    cJSON *json = cJSON_Parse(json_f_buffer);
    char *string = cJSON_Print(json);
    cJSON_Delete(json);
    printf("%s", string);
    return 0;
}
