from cgi import print_form
from fileinput import filename
import subprocess
import argparse
import glob
import io
import sys
import difflib
import os

def main():
    parser = argparse.ArgumentParser(description="Clang format runner, diff finder\n")
    parser.add_argument("-f", "--full", help="formal all source files, not only git diff files", action="store_true")
    args = parser.parse_args()

    if args.full:
        files = glob.glob("./src/**/*.[ch]", recursive=True)

    else:
        files = getGitDiff()
    
    returnValue = compare(files)
    if returnValue == 0:
        sys.exit(0)
    else:
        sys.exit(1)

def printFiles(files):
    print("List of files that will compare:\n")
    for file in files:
        print("%s" % file)

def getGitDiff():
    proc = subprocess.Popen(["git", "diff", "--name-only", "--no-color", "HEAD^"], stdout=subprocess.PIPE, stderr=None, stdin=subprocess.PIPE, universal_newlines=True)
    stdout, stderr = proc.communicate()
    if proc.returncode != 0:
        sys.exit(proc.returncode)

    files = io.StringIO(stdout).readlines()

    new_files = []
    for file in files:
        line = file.replace('\n', '', 1)
        if line.endswith('.c') or line.endswith('.h'):
            new_files.append(line)

    return new_files

def compare(files):
    if len(files) == 0:
        return 0

    for file in files:
        with io.open(file, 'r') as f:
            code = f.readlines()
        proc = subprocess.Popen(["clang-format", "-Werror", "-style=file", file], stdout=subprocess.PIPE, stderr=None, stdin=subprocess.PIPE, universal_newlines=True)
        stdout, stderr = proc.communicate()
        if proc.returncode != 0:
            sys.exit(proc.returncode)

        filename = os.path.basename(file)
        
        formatted_code =io.StringIO(stdout).readlines()
        diff = difflib.unified_diff(code, formatted_code,
                                    filename, filename, 
                                    '(Before formatting)', '(After formatting)')
        diff_string = ''.join(diff)
        if len(diff_string) > 0:
            sys.stdout.write(diff_string)
            return 1
        else:
            return 0

if __name__ == "__main__":
    main()