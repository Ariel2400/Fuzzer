import json
import sys

if __name__ == '__main__':
    json_file = sys.argv[1]
    with open(json_file, 'r') as f:
        json_string = json.loads(f.read())
    print(json_string)
