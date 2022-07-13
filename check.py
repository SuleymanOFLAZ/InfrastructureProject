import subprocess
import sys
import argparse
import glob
import os
import io

code_path = "./src"
cppCheckBuild_dir = "./cppcheck/cppCheckBuild"
include_path = "./src/include"

command = ["cppcheck"]
arguments = ["--dump", "--enable=all", "--platform=./cppcheck/aix_ppc64.xml",
                "--library=./cppcheck/posix.cfg", "--inconclusive",
                "--suppressions-list=./cppcheck/suppressions.txt",
                "--addon=./cppcheck/misraAddon/misraRule.json",
                "--includes-file=./cppcheck/includeFiles.txt",
                "--error-exitcode=1",
                ]

parser = argparse.ArgumentParser(description="CppCheck Script.\n")
parser.add_argument("-CC", "--checkconfig", help="Check Cppcheck's Configuration. The real cppcheck analysis operation doesn't run with this argument, only cppheck configurations will be checked.", action="store_true")
parser.add_argument("-CL", "--checklibrary", help="Check Cppcheck's Library Configuration. The real cppcheck analysis operation doesn't run with this argument, only cppheck library configurations will be checked.", action="store_true")
parser.add_argument("-CBD", "--cleanbuilddir", help="Cleans Cppheck build directory that contains information about last check. Than runs command with clean directory.", action="store_true")
parser.add_argument("-GD", "--gitdiff", help="Only check files that changed after last git commit, using gir diff.", action="store_true")
args = parser.parse_args()

# Get all .h file paths
incFiles = glob.glob("./src/**/*.h", recursive=True)

# Convert into only directories
incDir = []
for files in incFiles:
    incDir.append(os.path.dirname(files))

# Remove duplicate ones
incDir = list(set(incDir))

# Create Command
if args.checkconfig:
    arguments.append("--check-config")
elif args.checklibrary:
    arguments.append("--check-library")
else:
    arguments.append("--cppcheck-build-dir=./cppcheck/cppCheckBuild")
command.extend(arguments)

# Check that git diff or whole files
if args.gitdiff:
    proc = subprocess.Popen(["git", "diff", "--name-only", "--no-color", "HEAD^"], stdout=subprocess.PIPE, stderr=None, stdin=subprocess.PIPE, universal_newlines=True)
    stdout, stderr = proc.communicate()
    if proc.returncode != 0:
        sys.exit(proc.returncode)

    files = io.StringIO(stdout).readlines()

    new_files = []
    for file in files:
        line = file.replace('\n', '', 1)
        if line.endswith('.c'):
            new_files.append(line)
    
    if len(new_files) == 0:
        print ("There is no changed source file after last commit\n")
        sys.exit(0)
    else:
        for files in new_files:
            command.append(files)
else:
    command.append(code_path)
for dir in incDir:
    include_argument = "-I"+dir
    command.append(include_argument)

# Clean cppcheck build dir if clean run needed
if args.cleanbuilddir:
    for file in os.listdir('./cppcheck/cppCheckBuild'):
        os.remove(os.path.join('./cppcheck/cppCheckBuild', file))

# Call subprocess
proc = subprocess.Popen(command,
                            stdout=subprocess.PIPE, 
                            stderr=None, 
                            stdin=subprocess.PIPE, 
                            universal_newlines=True)
stdout, stderr = proc.communicate()
print(stdout)

# Remove .dump files
dumpFiles = glob.glob("./src/**/*.dump", recursive=True)
if len(dumpFiles) != 0:
    for files in dumpFiles:
        os.remove(files)

if proc.returncode != 0:
    sys.exit(proc.returncode)