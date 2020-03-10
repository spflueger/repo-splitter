### Note
It is adviced to use [git filter-repo](https://github.com/newren/git-filter-repo) instead of git filter-branch (which is also used in this repo)

### How to use

This script helps moving specific files from one repo into new one (including full history)
It creates a small shell script that can be used when running the `git filter-branch` command.

1. Run `python generateMoveScript.py --newroot path/you/want/to/strip/away /path/to/your/repo/root paths/to/move`
  This creates a shell script `movescript.sh` that is used in the second step.

2. `chmod u+x /path/to/script`

3. Change directory into your repo that you want to move from, then run 
  `git filter-branch -f --prune-empty --tree-filter /path/to/script HEAD`
  You can verify the new log via `git log`

4. Now actually make the changes by running `git filter-branch --prune-empty -f --subdirectory-filter newroot`

5. If everything is good push to your new repo
