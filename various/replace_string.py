#!/bin/env python

# replace strings in a file, even if they contain whitespaces
#
# Just like sed, but without the need to escape all those whitespaces.
# Note that the input file will be overwritten.
# Example:
# > replace_string.py file.txt "foo baz" "bar bat"
#
# davide.gerbaudo@gmail.com
# Apr 2015

import re
import sys

def main():
    if len(sys.argv)<4:
        print 'Usage:\n{} file.txt "string from" "string to"'.format(sys.argv[0])
        return
    input_file = sys.argv[1]
    string_from = clean_quotes(sys.argv[2])
    string_to = clean_quotes(sys.argv[3])
    lines = []
    with open(input_file, 'r') as sources:
        lines = sources.readlines()
    with open(input_file, 'w') as sources:
        for line in lines:
            sources.write(line.replace(string_from, string_to))
            # sources.write(re.sub(string_from, string_to, line))

def clean_quotes(s):
    if s.startswith('"') and s.endswith('"'):
        s = eval(s)
    if s.startswith("'") and s.endswith("'"):
        s = eval(s)
    return s
if __name__=='__main__':
    main()
