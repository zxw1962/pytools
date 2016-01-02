#!/usr/bin/env python
# coding=utf-8
import sys
import subprocess


def del_branch(branch_name):
    del_branch_local = "git branch -D " + branch_name
    print 'del_branch_local = %s' % del_branch_local
    result = subprocess.call(del_branch_local, shell=True)
    if result == 0:
        # begin to del remote branch only when del local is successful
        del_branch_remote = "git push origin :" + branch_name
        print 'del_branch_remote = %s' % del_branch_remote
        subprocess.call(del_branch_remote, shell=True)

if __name__ == "__main__":
    argvLen = len(sys.argv)
    if argvLen == 1:
        print "supply some branch_names..."
        sys.exit(1)

    args = sys.argv[1:]  # except file name from command line
    for name in args:
        del_branch(name)
