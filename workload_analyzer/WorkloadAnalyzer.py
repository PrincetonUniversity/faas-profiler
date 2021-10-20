#!/usr/bin/env python3

# Copyright (c) 2019 Princeton University
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

# Standard
from datetime import datetime
import json
from optparse import OptionParser
import os
from os.path import isfile, join
import pandas as pd
import pickle
import sys

# Local
sys.path = ['./', '../'] + sys.path
from GenConfigs import *
sys.path = [FAAS_ROOT, FAAS_ROOT+'/commons', FAAS_ROOT+'/workload_analyzer'] + sys.path
from Logger import ScriptLogger
from PerfMonAnalyzer import *
from TestDataframePlotting import *

logger = ScriptLogger(loggername='workload_analyzer',
                      logfile='WA.log')


def GetTestMetadata(test_metadata_file=FAAS_ROOT+"/synthetic_workload_invoker/test_metadata.out"):
    """
    Returns the test start time from the output log of SWI.
    """
    test_start_time = None
    with open(test_metadata_file) as f:
        lines = f.readlines()
        test_start_time = lines[0]
        config_file = lines[1]
        invoked_actions = int(lines[2][:-1])
        print('Invocations by Workload Invoker :' + str(invoked_actions))
    try:
        return int(test_start_time[:-1]), config_file[:-1]
    except:
        logger.error("Error reading the test metadata!")
        return None, None


def ExtractExtraAnnotations(json_annotations_data):
    """
    Extracts deep information from activation json record.
    """
    extra_data = {'waitTime': [], 'initTime': [], 'kind': []}

    for item in json_annotations_data:
        if item['key'] in extra_data.keys():
            extra_data[item['key']] = item['value']

    for key in extra_data.keys():
        if extra_data[key] == []:
            extra_data[key] = 0

    return extra_data


def ConstructConfigDataframe(config_file):
    """
    Returns a dataframe which describes the test in a standard format.
    """
    workload = None
    try:
        with open(config_file) as f:
            workload = json.load(f)
            logger.info("Successfully read the specified workload")
    except:
        logger.error("The JSON config file cannot be read")
        return False

    return [workload['test_name'], pd.DataFrame(workload['instances']).transpose()]


def ConstructTestDataframe(since, limit=1000, read_results=False):
    """
    Constructs a dataframe for the performance information of all invocations.
    """
    from ContactDB import GetActivationRecordsSince
    perf_data = {'func_name': [], 'activationId': [], 'start': [], 'end': [
    ], 'duration': [], 'waitTime': [], 'initTime': [], 'latency': [], 'lang': []}
    if read_results:
        perf_data['results'] = []

    activations = GetActivationRecordsSince(since=since, limit=limit)
    if 'error' in activations.keys():
        print('Encountered an error getting data from the DB! Check the logs for more info.')
        logger.error('DB error: ' + activations['reason'])
        return None
    activations = activations['docs']

    for activation in activations:
        if 'invokerHealthTestAction' in activation['name']:
            continue    # skipping OpenWhisk's health check invocations
        perf_data['func_name'].append(activation['name'])
        perf_data['activationId'].append(activation['_id'])
        perf_data['start'].append(activation['start'])
        perf_data['end'].append(activation['end'])
        perf_data['duration'].append(activation['duration'])
        extra_data = ExtractExtraAnnotations(
            activation['annotations'])
        perf_data['waitTime'].append(extra_data['waitTime'])
        perf_data['initTime'].append(extra_data['initTime'])
        perf_data['lang'].append(extra_data['kind'])
        perf_data['latency'].append(
            perf_data['duration'][-1]+perf_data['waitTime'][-1])
        if read_results:
            perf_data['results'].append(activation['response']['result'])

    return pd.DataFrame(perf_data)


def CreateStatisticalSummary(test_df, config_df, test_start_time):
    """
    This function returns a dataframe including the statistical
    summary of functions invoked in this test.
    """
    summary = {'func_name': [], 'rate': [], 'throughput': [], 'rel_stress': []}
    functions = set(test_df['func_name'])

    for function in functions:
        summary['func_name'].append(function)
        try:
            rate = config_df[config_df['application']
                             == function]['rate'].tolist()
            start = config_df[config_df['application']
                              == function]['activity_window'].tolist()
            rate, start = rate[0], test_start_time + 1000.0*start[0][0]
        except:
            rate, start = None, float('inf')
        summary['rate'].append(rate)
        partial_df = test_df[test_df['func_name'] == function]
        start_time = min(partial_df['start'].min(), start)
        try:
            throughput = 1000.0 * \
                len(partial_df['start'])/(partial_df['end'].max() - start_time)
        except:
            throughput = 0
        summary['throughput'].append(throughput)
        try:
            summary['rel_stress'].append(1.0*rate/throughput)
        except:
            summary['rel_stress'].append(None)

    return pd.DataFrame(summary)


def NormalizeMemoryValue(mem_string):
    """
    Returns memory value in Gigabyte
    """
    if mem_string[-1] == 'G':
        return float(mem_string[:-1])
    elif mem_string[-1] == 'M':
        return float(mem_string[:-1])/1024.0
    elif mem_string[-1] == 'K':
        return float(mem_string[:-1])/(1024*1024.0)


def GetSystemdCgtopDetails(file_path):
    """
    Returns details from a systemd-cgtop record.
    """
    container_count = 0
    docker_tasks = 0
    with open(file_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            reduced = line.split(' ')
            reduced = [r for r in reduced if r != '']
            if 'docker/' in line:
                container_count += 1
                try:
                    docker_tasks += int(reduced[1])
                except:
                    pass
            elif 'docker.service' in line:
                memory = NormalizeMemoryValue(reduced[3])

    return {'container_count': container_count,
            'docker_tasks': docker_tasks, 'memory': memory}


def GetControlGroupsRecords(since=None):
    """
    Reads the systemd-cgtop records.
    """
    cgroups_rec = {'timestamp': [], 'container_count': [],
                   'docker_tasks': [], 'memory': []}
    if since == None:
        logger.error("No since parameter entered!")
        return None
    log_path = FAAS_ROOT+'/logs'
    scg_files = [f for f in os.listdir(log_path) if (
        isfile(join(log_path, f))) and ('systemd-cgtop' in f)]

    # only keep the recent records
    scg_files = [f for f in scg_files if int(
        f[f.index('_')+1:f.index('.')]) >= since]

    if len(scg_files) == 0:
        logger.info(
            "There are no applicable systemd-cgtop records in the logs directory.")
        return None

    for scg_file in scg_files:
        time_stamp = scg_file[scg_file.index('_')+1:scg_file.index('.')]
        cgroups_rec['timestamp'].append(time_stamp)
        rec_details = GetSystemdCgtopDetails(log_path+'/'+scg_file)
        cgroups_rec['container_count'].append(rec_details['container_count'])
        cgroups_rec['docker_tasks'].append(rec_details['docker_tasks'])
        cgroups_rec['memory'].append(rec_details['memory'])

    return pd.DataFrame(cgroups_rec)


def CapacityFactor(test_df):
    """
    Returns the capacity factor for a workload, meaning how much
    it is stressing the system based on invocation latencies.
    """
    capacity_factors = {}
    functions = set(test_df['func_name'])
    for function in functions:
        temp_data = test_df[test_df['func_name'] == function]
        capacity_factors[function] = temp_data['latency'].quantile(
            0.9) - temp_data['latency'].quantile(0.1)

    print('CapacityFactor: ' + str(capacity_factors))
    return capacity_factors


def main(argv):
    """
    The main function.
    """
    parser = OptionParser()
    parser.add_option("-v", "--verbose", dest="verbose",
                      help="prints the detailed test data", action='store_true')
    parser.add_option("-p", "--plot", dest="plot",
                      help="plots the test results", action='store_true')
    parser.add_option("-s", "--save_plot", dest="save_plot",
                      help="save test result plots", action='store_true')
    parser.add_option("-a", "--archive", dest="archive",
                      help="archive the test results in an pickle file", action='store_true')
    parser.add_option("-c", "--capacity_factor", dest="capacity_factor",
                      help="returns the capacity factor", action='store_true')
    parser.add_option('-o', '--override_testname', dest='override_testname',
                      help='override the JSON test name', metavar='FILE')
    parser.add_option("-r", "--read_results", dest="read_results",
                      help="gather also the results of function invocations", action='store_true')
    (options, args) = parser.parse_args()

    logger.info("Workload Analyzer started")
    print("Log file -> logs/WA.log")

    test_start_time, config_file = GetTestMetadata()
    if FAAS_ROOT in config_file:
        [test_name, config_df] = ConstructConfigDataframe(config_file)
    else:
        [test_name, config_df] = ConstructConfigDataframe(
            FAAS_ROOT + '/' + config_file)

    read_results = True if options.read_results else False
    test_df = ConstructTestDataframe(since=test_start_time, limit=100000,
                                     read_results=read_results)
    if (test_df is None):
        logger.error('Test result dataframe could not be constructed!')
        return False
    print('Records read from CouchDB: ' + str(len(test_df['start'])))
    print('Test Dataframe:')
    print(test_df)

    invocation_periods = []
    start_times = []
    for index, row in test_df.iterrows():
        start_time = row['start']
        start_times.append(start_time)
    sorted_starts = sorted(start_times)
    invocation_periods = [sorted_starts[i+1] - sorted_starts[i]
                          for i in range(len(sorted_starts) - 1)]
    try:
        mean_invocation_period = 1.0 * \
            sum(invocation_periods)/len(invocation_periods)
        print('invocation period: ' + str(mean_invocation_period))
        print('avg invocation rate: ' + str(1000.0/mean_invocation_period))
    except:
        print('No invocations found!')

    stat_df = CreateStatisticalSummary(test_df, config_df, test_start_time)
    print(stat_df)

    if options.override_testname:
        # override the testname
        test_name = options.override_testname

    ref = test_df['start'].min()
    test_df['start'] -= ref
    test_df['end'] -= ref
    cgroups_df = GetControlGroupsRecords(since=test_start_time)
    perf_mon_records = AnalyzePerfMonRecords(config_file)
    test_df['execution'] = test_df['duration'] - test_df['initTime']

    if options.verbose:
        # Printing the data
        print(config_df)
        print(stat_df)
        print(test_df)
        print(cgroups_df)
        print(perf_mon_records)
    if options.plot:
        # Plotting the data
        if options.save_plot:
            save_plot = True
        else:
            save_plot = False
        TestDataframePlotter(save_plot, test_df, cgroups_df)
        # PerfMonPlotter(perf_mon_records, time_window=[5, 10])
    if options.archive:
        # Storing the data
        now = datetime.now()
        file_name = FAAS_ROOT + '/data_archive/' + now.strftime("%Y_%m_%d_%H_%M") + \
            '_' + test_name + '.pkl'
        pickle.dump([test_name, config_df, stat_df, test_df,
                     perf_mon_records], open(file_name, "wb"))
    if options.capacity_factor:
        with open(FAAS_ROOT + '/workload_analyzer/capacity_factors.json', 'w') as outfile:
            json.dump(CapacityFactor(test_df), outfile)

    print('Performance Summary')
    for dim in ['initTime', 'execution', 'latency']:
        print('Mean ' + dim + ' (ms): ' + str(test_df[dim].mean()))
        print('Std ' + dim + ' (ms): ' + str(test_df[dim].std()))
        print('***********')
    warm_starts_test_df = test_df[test_df['initTime'] == 0]
    print('Warm Start Performance Summary (count: ' +
          str(len(warm_starts_test_df[dim])) + ')')
    for dim in ['initTime', 'execution', 'latency']:
        print('Mean ' + dim + ' (ms): ' + str(warm_starts_test_df[dim].mean()))
        print('Std ' + dim + ' (ms): ' + str(warm_starts_test_df[dim].std()))
        print('***********')
    cold_starts_test_df = test_df[test_df['initTime'] != 0]
    print('Cold Start Performance Summary (count: ' +
          str(len(cold_starts_test_df[dim])) + ')')
    for dim in ['initTime', 'execution', 'latency']:
        print('Mean ' + dim + ' (ms): ' + str(cold_starts_test_df[dim].mean()))
        print('Std ' + dim + ' (ms): ' + str(cold_starts_test_df[dim].std()))
        print('***********')

    return True


if __name__ == "__main__":
    main(sys.argv)
