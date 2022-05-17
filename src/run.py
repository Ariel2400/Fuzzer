import sys


def main():
    command_line_args = sys.argv[1:]
    fuzz_type = command_line_args[0]
    fuzz_args = command_line_args[1:]

    if fuzz_type == "mutation":
        pass
    elif fuzz_type == "generation":
        pass
    elif fuzz_type == "symbolic_execution":
        pass


if __name__ == '__main__':
    main()