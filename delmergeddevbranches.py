#!/usr/bin/env python
# coding=utf-8

import sys
import subprocess
import time

target_remote_branch_prefix = 'dev_'
one_week_in_seconds = 7 * 24 * 60 * 60


def get_existed_remote_branches():

    """
        返回远端存在超过1周(以最后一个commit提交的时间计算)且以dev_开头的分支

        'git ls-remote --heads' sample output:

        From http://gitlab.xxx.org/xxx/xxx.git
        30c1b7b23580e0c445522893d96cb1a4e232ac03       	refs/heads/dev_xiaochuang_20160113_mission_m
        99d72cfd72dec4b57b0096811a995231e10790dc       	refs/heads/master
        d397dbf770bac70fd6262491856dd959d8fc65f6       	refs/heads/release
        6ff1a30820ea79725802cc9cfcea92adcf251226       	refs/heads/release_v811
    """

    branches = []
    global target_remote_branch_prefix
    global one_week_in_seconds

    try:
        output = subprocess.check_output(['git', 'ls-remote', '--heads'])
        # print output
        if output != '':
            res = output.split('\n')
            current_time = time.time()
            # print res
            for row in res:
                if '\t' in row and target_remote_branch_prefix in row:
                    elements = row.split('\t')
                    if len(elements) < 2:
                        continue
                    last_commit_time = get_last_commit_time_in_second(elements[0], current_time)
                    # print current_time, last_commit_time
                    sencond_ele = elements[1]
                    if current_time - last_commit_time >= one_week_in_seconds:
                        branches.append(sencond_ele[sencond_ele.find(target_remote_branch_prefix):])
    except subprocess.CalledProcessError as error:
        print "exception occurs when call 'git ls-remote --heads', maybe not in a git repo."
        sys.exit(1)

    return branches


def get_last_commit_time_in_second(commit_id, current_time):

    try:
        output = subprocess.check_output(['git', 'show', '-s', '--format=%ct', commit_id])
        time_in_second = float(output)

    except subprocess.CalledProcessError:
        time_in_second = current_time
        print "exception occurs when call 'git show -s --format=%ct %s'" % commit_id

    return time_in_second


def get_merged_remote_branches():

    """
        'git branch -r --merged origin/master' sample output:

        origin/dev_amiao_160713_rename_component
        origin/dev_wenzhi160801_basesdk
        origin/dev_yunkong_1203_attr
        origin/master
        origin/release
    """

    branches = []
    global target_remote_branch_prefix

    try:
        output = subprocess.check_output(['git', 'branch', '-r', '--merged', 'origin/master'])
        # print output
        if output != '':
            res = output.split('\n')
            branches = [x[x.find(target_remote_branch_prefix):] for x in res if target_remote_branch_prefix in x]
    except subprocess.CalledProcessError as error:
        print "exception occurs when call 'git branch -r --merged origin/master', maybe not in a git repo."
        sys.exit(2)

    return branches


def del_remote_branch(branch_name):
    del_branch_remote = "git push origin :" + branch_name
    print 'del_branch_remote = %s' % del_branch_remote
    subprocess.call(del_branch_remote, shell=True)

if __name__ == "__main__":

    existed_remote_branches = get_existed_remote_branches()
    merged_remote_branches = get_merged_remote_branches()

    # print len(existed_remote_branches)
    # print existed_remote_branches
    # print len(merged_remote_branches)
    # print merged_remote_branches

    deletingBranches = [branch for branch in existed_remote_branches if branch in merged_remote_branches]
    if len(deletingBranches) == 0:
        print 'Congratulations, no dev_xxx branch need to delete...'
        sys.exit(0)
    print deletingBranches
    prompt = 'all these %d branches will be deleted, press y to continue? ' % len(deletingBranches)
    inputValue = raw_input(prompt)
    if inputValue == 'y':
        print 'starting delete...'
        for branch_name in deletingBranches:
            del_remote_branch(branch_name)
        print 'delete done...'
    else:
        print 'give up deleting branches...'
