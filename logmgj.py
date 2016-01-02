#!/usr/bin/env python
# coding=utf-8
import sys
import subprocess

if __name__ == "__main__":
    result = subprocess.check_output('adb shell "ps|grep com.mogujie$"', shell=True)
    print 'result = %s' % result
    if result:
        strs = result.split()
        size = len(strs)
        if size > 1:
            pid = strs[1]
            print 'pid = %s' % pid
        else:
            print 'cannot find valid pid...'
            sys.exit(1)

    if 'pid' in locals():
        logcmd = 'adb logcat -v time | grep "(%s"' % pid
        try:
            subprocess.call(logcmd, shell=True)
        except KeyboardInterrupt:
            pass
    else:
        print 'cannot find pid definition!!!'
