#!/usr/bin/python3 -ttu

import sys

def decode_cpuinfo(cpuinfofile):
    cpulist = []
    with open(cpuinfofile, 'r') as cpuinfo:
        cpudata = {}
        for entry in cpuinfo:
            #print("Original data: " + entry.strip())
            if ':' in entry:
                label, values = entry.split(':', 1)
                label = label.strip()
                if label == 'processor':
                    cpudata = {}
                cpudata[label] = values.strip()
            else:
                # End of CPU entry
                cpudata[label] = values.strip() 
                if len(cpudata) > 0:
                    cpulist.append(cpudata)
                    #print(cpudata)
    return cpulist

if __name__ == '__main__':
    if len(sys.argv) > 1:
        cpuinfofile = sys.argv[1]
    else:
        cpuinfofile = '/proc/cpuinfo'
    data = decode_cpuinfo(cpuinfofile)
    print(data)