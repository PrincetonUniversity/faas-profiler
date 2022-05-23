#!/usr/bin/env python3

# Copyright (c) 2019 Princeton University, 2022 UBC
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from datetime import datetime
import imp
from optparse import OptionParser
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes, mark_inset, zoomed_inset_axes, InsetPosition
import os
import pandas as pd
import pickle
import seaborn as sns
import sys
import time

sys.path = ['./', '../'] + sys.path

# Local
from GenConfigs import *
from commons.Logger import ScriptLogger

logger = ScriptLogger(loggername='comparative_analyzer', logfile='CA.log')
archive_folder = FAAS_ROOT + "/data_archive/"


def GetTimeFromDFName(dfname=None):
    if (dfname is None):
        raise ValueError("No dfname is provided, or dfname is None!")
    res = dfname[0:16]
    res = datetime.strptime(res, '%Y_%m_%d_%H_%M')
    return res


def ComparativePlotting(t_df, p_df_dic):
    """
    Plotting result comparisons.
    """
    dims = {'s': 'start', 'd': 'duration',
            'wt': 'waitTime', 'it': 'initTime', 'l': 'latency'}
    t_df['execution'] = t_df['duration'] - t_df['initTime']

    t_df['start'] = t_df['start']/1000.0
    t_df['latency'] = t_df['latency']/1000.0

    if p_df_dic is not None:
        p_df = p_df_dic['perf_records']

    ### ADD NEW DIMENSIONS TO THE DATA IF NEEDED
    # examples:
    # p_df['IPC'] = p_df['instructions']/p_df['cycles']
    # p_df['Page Faults per Million Instruction'] = 1000000.0*p_df['page-faults']/p_df['instructions']

    ### ADD YOUR PLOTTING CODE HERE
    # below code is just an example:
    sns.scatterplot(data=t_df, x='start', y='latency', hue='test')

    plt.savefig('sample_comparative_plot.png')
    plt.close()


def CompareArchives(archive_files, plot):
    """
    This function compares archived result of tests.
    """
    all_data = {}
    for entry in archive_files:
        pickle_file = archive_folder + entry[0]
        try:
            [test_name, config_df, stat_df, test_df, perf_mon_records] = \
                pickle.load(open(pickle_file, "rb"))
        except:
            logger.error("Issues reading archive pickle file " + pickle_file)
            return False

        name_mapping = {'json_dumps_8ps': 'D', 'json_dumps_50ps': 'C',
                        'json_dumps_100ps': 'A', 'json_dumps_66ps': 'B'}

        try:
            test_df['test'] = test_name
            # test_df['test'] = name_mapping[test_name]
            stat_df['test'] = test_name
        except:
            # means that the read archive is not among tests we're interested in
            print('Skipping ' + str(test_name))
            continue

        stat_df['Test Category'] = GetRawTestName(test_name)

        for k, v in perf_mon_records.items():
            v['test'] = test_name  # name_mapping[test_name]
            v['Test Category'] = GetRawTestName(test_name)

        applications = config_df['application']
        for application in applications:
            try:
                application_short = application[application.index('/')+1:]
            except:
                application_short = application
            t_df = test_df[test_df['func_name'] == application_short]
            distribution = config_df[config_df['application']
                                     == application]['distribution'][0]
            rate = config_df[config_df['application']
                             == application]['rate'][0]

            t_df['distribution'] = distribution
            t_df['rate'] = rate

            try:
                throughput = 1000.0*len(t_df['start']) / \
                    (t_df['end'].max() - t_df['start'].min())
            except:
                throughput = 0

            t_df['start'] -= t_df['start'].min()

            # Concatenating the test DF for each application
            try:
                combined_test_df = pd.concat([combined_test_df, t_df])
            except:
                combined_test_df = t_df

        # Concatenating the perf DF for each test
        try:
            for key in perf_mon_records.keys():
                combined_perf_df_dic[key] = pd.concat(
                    [combined_perf_df_dic[key], perf_mon_records[key]])
        except:
            combined_perf_df_dic = perf_mon_records

        # Concatenating the Stats DF
        try:
            combined_stat_df = pd.concat([combined_stat_df, stat_df])
        except:
            combined_stat_df = stat_df

    try:
        keys = combined_perf_df_dic.keys()
    except:
        combined_perf_df_dic = None

    return [combined_test_df, combined_perf_df_dic, combined_stat_df]


def GetRawTestName(test_name):
    """
    Remove the test to be able to compare tests of the same category.
    TODO-> This should be generalized
    """
    raw_test_name = test_name
    while True:
        if 'ps' not in raw_test_name:
            break

        end_pointer = raw_test_name.index('ps')
        start_pointer = raw_test_name.index('_', end_pointer - 4) + 1
        if (end_pointer - start_pointer) > 0:
            raw_test_name = raw_test_name[:start_pointer] + \
                raw_test_name[end_pointer:]
            raw_test_name = raw_test_name.replace('ps', '', 1)

    return raw_test_name


def RelativeDegradation(combined_stat_df):
    """
    This function analyzes the relative degradation of one or more functions.
    """
    # print(combined_stat_df)
    fig, axs = plt.subplots(ncols=1, sharex=True)
    # combined_stat_df.plot(kind='scatter', x='rate', y='rel_stress',
    #         alpha=0.5, marker='o', ax=axs[0])
    # combined_stat_df.plot(kind='line', x='rate', y='throughput',
    #         alpha=0.5, marker='o', ax=axs[1])
    # sns.relplot(data=combined_stat_df, x='rate',
    #             y='throughput', ax=axs[1], kind='line')
    function_of_interest = 'rand_vector_loop_d'
    test_cats = set(combined_stat_df['Test Category'])
    for test_cat in test_cats:
        df = combined_stat_df[combined_stat_df['Test Category'] == test_cat]
        df = df[df['func_name'] == function_of_interest]
        sns.regplot(data=df, x='rate', y='throughput',
                    ax=axs, order=2, truncate=True)

    plt.xlabel('test')
    plt.ylabel('Function Throughput')
    plt.show()
    plt.close()


def main(argv=None):
    """
    The main function.
    """
    parser = OptionParser()
    parser.add_option('-s', '--since', dest='since',
                      help='compare archives since time', action='store_true')
    parser.add_option('-p', '--plot', dest='plot',
                      help='plots default comparative test results', action='store_true')
    parser.add_option('-c', '--customized_plot', dest='customized_plot',
                      help='specify a customized plotting string', metavar='FILE')
    (options, args) = parser.parse_args()

    logger.info("Comparative Analyzer started")
    print("Log file -> logs/CA.log")

    ls_files = os.popen("ls -l " + FAAS_ROOT + "/data_archive/*.pkl")
    archive_files = []
    for line in ls_files:
        archive_files.append([line[line.index('data_archive')+13:-1], None])
        archive_files[-1][1] = GetTimeFromDFName(archive_files[-1][0])

    if len(archive_files) == 0:
        logger.error("No test archive found in " + archive_folder + "!")
        return False

    if options.since:
        since = datetime.fromtimestamp(float(options.since)/1000)
        archive_files = [
            test_df_file for test_df_file in archive_files if test_df_file[1] > since]

    [combined_test_df, combined_perf_df_dic, combined_stat_df] = CompareArchives(
        archive_files, options.plot)

    if (options.plot) or (argv is None):
        ComparativePlotting(t_df=combined_test_df,
                            p_df_dic=combined_perf_df_dic)
    elif options.customized_plot is not None:
        cp = options.customized_plot.replace('.py', '')
        if '/' in cp:
            if cp[1] == '/':
                cp = cp[2:]
            cp = cp[cp.index('/') + 1:]
        module = __import__(cp)
        module.ComparativePlotting(t_df=combined_test_df, p_df_dic=combined_perf_df_dic)

    return True


if __name__ == "__main__":
    main(sys.argv)
