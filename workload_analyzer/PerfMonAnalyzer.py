# Copyright (c) 2019 Princeton University
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from datetime import datetime, timedelta
import json
import os.path
import pandas as pd
import sys

sys.path = ['./', '../'] + sys.path

# Local
from GenConfigs import *
from Logger import ScriptLogger

logger = ScriptLogger(loggername='workload_analyzer/perf_mon_analyzer',
                      logfile='WA.log')


def ReadPQOSMSRMon(pqos_msr_mon_file):
    """
    This function parses the output of the pqos-msr-mon.
    """
    with open(pqos_msr_mon_file) as f:
        lines = f.readlines()

    records = {'timestamp': [], 'Core': [], 'IPC': [],
               'LLC Misses': [], 'LLC Util (KB)': [], 'MBL (MB/s)': []}
    tmp_records = {'timestamp': [], 'Core': [], 'IPC': [],
                   'LLC Misses': [], 'LLC Util (KB)': [], 'MBL (MB/s)': []}
    prev_timestamp, index = None, -1

    for line_index in range(len(lines)):
        line = lines[line_index]
        if 'TIME' in line:
            index += 1
            timestamp = datetime.strptime(line[5:-1], '%Y-%m-%d %H:%M:%S')
            if (timestamp != prev_timestamp):
                for key, value in tmp_records.items():
                    if key == 'timestamp':
                        for i in value:
                            records[key] += [prev_timestamp +
                                             timedelta(seconds=1.0*i/index)]
                    else:
                        records[key] += value
                tmp_records = {'timestamp': [], 'Core': [], 'IPC': [
                ], 'LLC Misses': [], 'LLC Util (KB)': [], 'MBL (MB/s)': []}
                index = 0

            prev_timestamp = timestamp
        elif 'CORE' in line:
            pass
        else:
            tmp_records['timestamp'].append(index)
            separated = line.split(' ')
            separated = [v for v in separated if v != '']
            tmp_records['Core'].append(int(separated[0]))
            tmp_records['IPC'].append(float(separated[1]))
            tmp_records['LLC Misses'].append(int(separated[2][:-1])*1000)
            tmp_records['LLC Util (KB)'].append(float(separated[3]))
            tmp_records['MBL (MB/s)'].append(float(separated[4]))

    for key, value in tmp_records.items():
        if key == 'timestamp':
            for i in value:
                records[key] += [prev_timestamp +
                                 timedelta(seconds=1.0*i/index)]
        else:
            records[key] += value

    # return the records as Pandas dataframe
    records_df = pd.DataFrame(records)
    return records_df


def ReadPerfMon(perf_mon_file):
    """
    This function parses the output of the Linux Perf tool.
    """
    with open(perf_mon_file) as f:
        lines = f.readlines()

    records = {'timestamp': []}          # more fields are added dynamically

    for line in lines:
        separated = line.split(' ')
        separated = [v for v in separated if v != '']

        try:
            if 'counted' in separated[2]:
                del separated[2]
        except:
            pass

        if (len(separated) < 3) or (len(separated) > 4):
            continue
        time = float(separated[0])
        field = separated[2]
        try:
            val = int(separated[1].replace(',', ''))
        except:
            val = None
        try:
            records[field].append(val)
        except:
            records[field] = [val]      # first element of the list
        try:
            if records['timestamp'][-1] != time:
                records['timestamp'].append(time)
        except:
            records['timestamp'].append(time)   # first append

    # return the records as Pandas dataframe
    return pd.DataFrame(records)


def AnalyzePerfMonRecords(config_file):
    """
    This function is used to analyze the performance monitoring data after conducting the test.
    """
    logger.info("Started to analyze the performance monitoring records.")

    try:
        with open(FAAS_ROOT + '/' + config_file) as f:
            workload = json.load(f)
    except:
        return False

    records = {}

    # Perf Tool
    perf_mon_file = FAAS_ROOT + '/perf-mon.out'
    pqos_msr_mon_file = FAAS_ROOT + '/pqos-msr-mon.out'

    if not os.path.isfile(perf_mon_file):
        logger.error("The perf output file missing!")
    else:
        records['perf_records'] = ReadPerfMon(perf_mon_file)

    # PQOS Mon
    if not os.path.isfile(pqos_msr_mon_file):
        logger.error("The PQOS output file is missing!")
    else:
        records['pqos_records'] = ReadPQOSMSRMon(pqos_msr_mon_file)

    return records
