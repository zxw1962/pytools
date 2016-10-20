#!/usr/bin/env python
# coding=utf-8
import sys
import subprocess


def getalltags():
    res = []
    try:
        output = subprocess.check_output(['git', 'tag'])
        if output != '':
            res = output.split('\n')
    except subprocess.CalledProcessError as error:
        # print 'exception occurs when call check_output: ' + error.message
        pass
    return res


def del_unneeded_tags(tags):
    if len(tags) == 0:
        print 'no tags found...'
        return
    del_tags_command = 'git tag -d '
    new_tags = [tag for tag in tags if len(tag) == 5 and not tag.startswith('v')]
    if len(new_tags) == 0:
        print 'no unneeded tags found...'
        return
    tmp = ' '.join(new_tags)
    final_del_unneeded_tags = del_tags_command + tmp
    print 'del unneeded tags = %s' % final_del_unneeded_tags
    subprocess.call(final_del_unneeded_tags, shell=True)

if __name__ == "__main__":
    del_unneeded_tags(getalltags())
