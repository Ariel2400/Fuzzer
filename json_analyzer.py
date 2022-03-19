import json


def check_for_duplicate_keys(json_dict: dict):
    buffer = {}

    for k, v in json_dict.items():
        if k in buffer:
            print(f'found duplicate key {k}')
            return
        else:
            buffer[k] = v


def check_for_key_collisions(json_dict: dict):
    dup = {}
    for k, v in json_dict.items():
        k_encoded = k.encode()
        dup[k_encoded] = v
    return check_for_duplicate_keys(dup)


def check_for_number_inconsitencies(json_dict):
    pass
