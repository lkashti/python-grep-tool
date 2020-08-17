import argparse
import re
import sys

from lib.formatter import (SimpleFormatter, MachineReadableFormatter,
                           ColoredFormatter)


def main():
    arguments = parse()
    # taking the raw string
    regex_to_compile = rf'{arguments.regex}'
    regex = re.compile(regex_to_compile)
    match_in_multiple_files(arguments.files, regex, arguments.color,
                            arguments.machine)
    sys.exit(0)


def match_in_multiple_files(files, regex, color, machine):
    """
    Searches for matches in one or more files.

    :param list files: file name stated in the command line
    :param re.Pattern regex: compiled regex object
    :param bool color: enable color format
    :param bool machine: enable machine readable format
    """
    for file_name in files:
        lines = read_file(file_name)
        match_in_file(file_name, lines, regex, color, machine)


def match_in_file(file_name, lines, regex, color, machine):
    """
    Searches for matches in a file and prints it line by line.

    :param str file_name: file to be searched for regex matches
    :param list lines: list of lines from the file
    :param re.Pattern regex: compiled regex object
    :param bool color: enable color format
    :param bool machine: enable machine readable format
    """
    for line_no, matched_line, regex_result, start_pos in search(lines, regex):
        # a formatter works on a single line at a time
        if color:
            print(ColoredFormatter(matched_line, regex_result).format(),
                  end='')
        elif machine:
            print(MachineReadableFormatter(file_name, line_no,
                                           matched_line, start_pos
                                           ).format(), end='')
        else:
            print(SimpleFormatter(file_name, line_no, matched_line).format(),
                  end='')
    print()


def search(lines, regex):
    """
    Searches for matches in a list of lines.
    :param list lines: list of lines from the file
    :param re.Pattern regex: compiled regex object
    """
    for line_no, line in enumerate(lines):
        # object that holds information about a match
        match_obj = re.search(regex, line)
        if match_obj:
            yield line_no, line, match_obj.group(), match_obj.start()


def read_file(file_name):
    try:
        with open(file_name, 'r') as file:
            return file.readlines()
    except FileNotFoundError as fnf:
        print(fnf)
        sys.exit(1)


def parse():
    """Returns a Namespace containing the command line arguments"""
    parser = argparse.ArgumentParser(
        usage='task.py [-c | -m] regex [FILE(S)...]')
    # positional args
    parser.add_argument('regex',
                        help='regex filter for pattern matching')
    parser.add_argument('files',
                        help='one or more file names',
                        nargs='+')  # print(file_name, "was not found.")
    # mutually exclusive optional args
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-c', '--color',
                       help='highlight matching text',
                       action='store_true')
    group.add_argument('-m', '--machine',
                       help='generate machine-readable output',
                       action='store_true')

    return parser.parse_args()


if __name__ == '__main__':
    main()
