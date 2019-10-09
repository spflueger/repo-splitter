import argparse
from pathlib import Path
import os
import subprocess

parser = argparse.ArgumentParser(description='')
parser.add_argument('repopath', type=str, nargs=1,
                    help='path to the git repo')
parser.add_argument('paths', type=str, nargs='+',
                    help='paths within the git repo to filter out from a repo into a new repo')
parser.add_argument('--strippath', type=str,
                    help='strip away this path from the new root')

args = parser.parse_args()

wd = os.getcwd()
os.chdir(args.repopath[0])
files_to_move={}
for path in args.paths:
    for filename in Path(path).glob('**/*.*'):
        files_to_move[filename] = []

for key in files_to_move.keys():
   vals = subprocess.check_output(["git log --name-only --format=format: --follow -- " + str(key) + " | sort -u"], shell=True)
   vals = [x.decode("utf-8") for x in vals.split()]
   files_to_move[key] = vals
os.chdir(wd)

if args.strippath:
    old_files = files_to_move
    files_to_move = {}
    for key, vals in old_files.items():
        newkey = str(key)
        if str(key).find(args.strippath) == 0:
            newkey = str(key)[len(args.strippath):]
        newkey = "newroot/" + newkey.strip("/")
        files_to_move[newkey] = vals

temp_dirs_to_create = [os.path.split(x)[0] for x in files_to_move]
dirs_to_create = set()
for tempdir in temp_dirs_to_create:
    if not [0 for x in temp_dirs_to_create if x != tempdir and x.find(tempdir) == 0]:
        dirs_to_create.add(tempdir)

f = open('movescript.sh', 'w')
f.write("#!/bin/bash\n\n")
for x in dirs_to_create:
    f.write("mkdir -p "+str(x)+"\n")
f.write("\n")
for key, vals in files_to_move.items():
    for val in vals:
        f.write("mv " + str(val) + " " + str(key)+" 2>/dev/null\n")
f.write("\ntrue")
f.close()