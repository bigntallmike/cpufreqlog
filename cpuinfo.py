#!/usr/bin/python3 -ttu

import sys

def decode_cpuinfo(cpuinfofile):
    with open(cpuinfofile, 'r') as cpuinfo:
        return decode_cpuinfo_stream(cpuinfo)

def decode_cpuinfo_stream(cpuinfo):
    cpulist, cpudata = [], {}
    for entry in cpuinfo:
        try:
            label, values = (_.strip() for _ in entry.split(':', 1))
            if label == 'processor':
                cpudata = {}
            cpudata[label] = values.strip()
        except ValueError:
            if len(cpudata):
                cpulist.append(cpudata)
    return cpulist

if __name__ == '__main__':
    if len(sys.argv) > 1:
        cpuinfofile = sys.argv[1]
    else:
        cpuinfofile = '/proc/cpuinfo'
    data = decode_cpuinfo(cpuinfofile)
    print(data)