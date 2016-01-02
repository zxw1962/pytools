#!/usr/bin/env python
# coding=utf-8
import sys
import subprocess
import time

if __name__ == "__main__":
    now = time.strftime("%y%m%d")
    new_branch_cmd = 'git checkout -b dev_chengfeng_' + now
    args = sys.argv;
    extra = ''
    size = len(args)
    if size == 2:
        extra = args[1]
    elif size > 2:
        print 'too many args supplied...just one is enough!!!'
        sys.exit(1)
    if extra != '':
        new_branch_cmd += '_' + extra
    #new_branch_cmd += ' master'
    subprocess.call(new_branch_cmd, shell=True)
