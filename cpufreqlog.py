#!/usr/bin/python3 -ttu

from cpuinfo import decode_cpuinfo
import os.path
import rrdtool
from time import sleep

RRDFILE = "/tmp/cpuinfo.rrd"
MAXCPUFREQ = 5000

def cpuinfo_loop():
    while True:
        cpu_info = decode_cpuinfo("/proc/cpuinfo")
        # Loop through the CPU list
        labels = []
        values = []
        for cpu_core_num, cpu_core_data in enumerate(cpu_info):
            labels.append(f"freq{cpu_core_num}")
            values.append(cpu_core_data['cpu MHz'])
        rrdtool.update(RRDFILE, "-t", 
                    ":".join(labels), 
                    "N:%s" % (":".join(values)))
        sleep(1)

# Optionally updatev returns an update such as:
# {'return_value': 0, '[1709587315]RRA[MIN][5]DS[freq0]': 1549.6820521280001, '[1709587315]RRA[MIN][5]DS[freq1]': 1549.6785453500001, '[1709587315]RRA[MIN][5]DS[freq2]': 1333.147248578, '[1709587315]RRA[MIN][5]DS[freq3]': 1299.4643400720001, '[1709587315]RRA[MIN][5]DS[freq4]': 1543.7737699590002, '[1709587315]RRA[MIN][5]DS[freq5]': 1544.8102617200002, '[1709587315]RRA[MIN][5]DS[freq6]': 1527.361015806, '[1709587315]RRA[MIN][5]DS[freq7]': 1546.8306707039999, '[1709587315]RRA[MIN][5]DS[freq8]': 1423.3740792560002, '[1709587315]RRA[MIN][5]DS[freq9]': 1549.691191004, '[1709587315]RRA[MIN][5]DS[freq10]': 1495.386679104, '[1709587315]RRA[MIN][5]DS[freq11]': 1280.4666312959998, '[1709587315]RRA[MIN][5]DS[freq12]': 1546.6821071279999, '[1709587315]RRA[MIN][5]DS[freq13]': 1546.874791215, '[1709587315]RRA[MIN][5]DS[freq14]': 1547.284018394, '[1709587315]RRA[MIN][5]DS[freq15]': 1532.394877984, '[1709587315]RRA[AVERAGE][5]DS[freq0]': 1549.9364104256001, '[1709587315]RRA[AVERAGE][5]DS[freq1]': 2181.6500065804003, '[1709587315]RRA[AVERAGE][5]DS[freq2]': 1465.8967161336, '[1709587315]RRA[AVERAGE][5]DS[freq3]': 1456.5358750616, '[1709587315]RRA[AVERAGE][5]DS[freq4]': 1547.4394051846, '[1709587315]RRA[AVERAGE][5]DS[freq5]': 1546.7518560126002, '[1709587315]RRA[AVERAGE][5]DS[freq6]': 1542.4505768656, '[1709587315]RRA[AVERAGE][5]DS[freq7]': 1548.1546073436, '[1709587315]RRA[AVERAGE][5]DS[freq8]': 1521.8619747405999, '[1709587315]RRA[AVERAGE][5]DS[freq9]': 2315.4968217718, '[1709587315]RRA[AVERAGE][5]DS[freq10]': 1535.7909230342, '[1709587315]RRA[AVERAGE][5]DS[freq11]': 1452.0023322665998, '[1709587315]RRA[AVERAGE][5]DS[freq12]': 1547.541721834, '[1709587315]RRA[AVERAGE][5]DS[freq13]': 1548.1530834888001, '[1709587315]RRA[AVERAGE][5]DS[freq14]': 1548.9047482124001, '[1709587315]RRA[AVERAGE][5]DS[freq15]': 1544.839795018, '[1709587315]RRA[MAX][5]DS[freq0]': 1550.0000000000002, '[1709587315]RRA[MAX][5]DS[freq1]': 2799.086920882, '[1709587315]RRA[MAX][5]DS[freq2]': 1549.685771438, '[1709587315]RRA[MAX][5]DS[freq3]': 1608.801761476, '[1709587315]RRA[MAX][5]DS[freq4]': 1549.699549936, '[1709587315]RRA[MAX][5]DS[freq5]': 1548.4291644640002, '[1709587315]RRA[MAX][5]DS[freq6]': 1546.892389463, '[1709587315]RRA[MAX][5]DS[freq7]': 1549.6428008900002, '[1709587315]RRA[MAX][5]DS[freq8]': 1549.6610195099997, '[1709587315]RRA[MAX][5]DS[freq9]': 3753.939765653, '[1709587315]RRA[MAX][5]DS[freq10]': 1549.9999999999998, '[1709587315]RRA[MAX][5]DS[freq11]': 1550.0000000000002, '[1709587315]RRA[MAX][5]DS[freq12]': 1549.6152050819999, '[1709587315]RRA[MAX][5]DS[freq13]': 1550.166761198, '[1709587315]RRA[MAX][5]DS[freq14]': 1550.0, '[1709587315]RRA[MAX][5]DS[freq15]': 1549.9999999999998}
#    or
# {'return_value': 0}

# NOTE: Could read /sys/devices/system/cpu/cpufreq/policy1/cpuinfo_max_freq for max instead
def setup_rrd():
    if not os.path.exists(RRDFILE):
        cpulist = decode_cpuinfo("/proc/cpuinfo")
        rrd_ds = [
            "RRA:MIN:0.5:5:1800",
            "RRA:AVERAGE:0.5:5:1800",
            "RRA:MAX:0.5:5:1800",
            "RRA:MIN:0.5:60:4320",
            "RRA:AVERAGE:0.5:60:4320",
            "RRA:MAX:0.5:60:4320",
            "RRA:MIN:0.5:3600:2160",
            "RRA:AVERAGE:0.5:3600:2160",
            "RRA:MAX:0.5:3600:2160",
                  ]
        for cpu_core_num in range(0, len(cpulist)):
            rrd_ds.append(f"DS:freq{cpu_core_num}:GAUGE:5:0:{MAXCPUFREQ}")
        #print(rrd_ds)
        rrdtool.create(RRDFILE, "--start", "now", "--step", "1", *rrd_ds)

if __name__ == "__main__":
    setup_rrd()
    try:
        cpuinfo_loop()
    except KeyboardInterrupt:
        print("Exiting")