#include <iostream>
#include <nlohmann/json.hpp>

int main(int argc, char const *argv[])
{
    json json = json::parse(argv[1])
    return 0;
}

// https://github.com/nlohmann/json#integration
// need to integrate it