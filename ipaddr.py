#!/usr/bin/env python
# coding=utf-8
import subprocess
import sys

if __name__ == "__main__":
    result = subprocess.check_output('ifconfig en0 |grep -w inet', shell=True)
    print 'output = %s' % result.strip()
    # result = None
    ip = ''
    if result:
        strs = result.split('\n')
        for line in strs:
            # remove \t, space...
            line = line.strip()
            if line.startswith('inet '):
                a = line.find(' ')
                ipStart = a+1
                ipEnd = line.find(' ', ipStart)
                if a != -1 and ipEnd != -1:
                    ip = line[ipStart:ipEnd]
                    break
    print 'ip = %s' % ip
