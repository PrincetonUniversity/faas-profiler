# Copyright (c) 2019 Princeton University
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from datetime import timedelta
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import sys

sys.path = ['./', '../'] + sys.path

# Local
from GenConfigs import *


def TestDataframePlotter(save_plot, test_df, cgroups_df=None, perf_mon_records=None):
    """
    This function is for plotting the test dataframe data.
    """
    fig, ax = plt.subplots(nrows=1, ncols=1)
    dims = {'s': 'start', 'd': 'duration',
            'wt': 'waitTime', 'it': 'initTime', 'l': 'latency'}

    print(test_df)

    color_palette = sns.color_palette('Set1')
    test_df.plot(kind='scatter', x=dims['s'], y=dims['d'],
                 c=color_palette[0], alpha=0.5, ax=ax, label='Run Time', marker='*')
    test_df.plot(kind='scatter', x=dims['s'], y=dims['it'],
                 c=color_palette[1], alpha=0.5, ax=ax, label='Initiation Time', marker='^')
    test_df.plot(kind='scatter', x=dims['s'], y=dims['wt'],
                 c=color_palette[2], alpha=0.5, ax=ax, label='Wait Time', marker='v')
    test_df.plot(kind='scatter', x=dims['s'], y=dims['l'],
                 c=color_palette[3], alpha=0.5, ax=ax, label='Total Latency', marker='o')
    ax.set_xlabel('Invocation Time (s)')
    ax.set_ylabel('Time (ms)')
    # sns.scatterplot(data=test_df, x=dims['s'], y=dims['wt'], hue='func_name', ax=ax, marker='v')
    # sns.scatterplot(data=test_df, x=dims['s'],
    #                 y='CTX_voluntary',
    #                 hue='func_name', ax=ax, marker='^')

    # if cgroups_df is None:
    #     fig, axs = plt.subplots(ncols=2)
    #     # axs = [axs]
    # else:
    #     fig, axs = plt.subplots(nrows=2)

    # sns.set(style="whitegrid")
    color_palette = sns.color_palette('Paired')

    # sns.relplot(data=test_df, x=dims['s'], y=dims['d'], \
    #                 hue='func_name', size=dims['wt'], \
    #                 alpha=.6, marker='o', ax=axs[0])
    # sns.relplot(data=test_df, x=dims['s'], y=dims['l'], \
    #                 hue='func_name', alpha=.6, marker='o', ax=axs[0])

    # sns.relplot(data=test_df, x=dims['s'], y='execution', \
    #                 hue='func_name', alpha=.6, marker='o', ax=axs[1])

    # axs[0].set_xlim([0, 15000])
    # axs[0].scatter(test_df['start'], test_df['latency'])

    # invocation_periods = []
    # start_times = []
    # for index, row in test_df.iterrows():
    #     start_time = row['start']
        # start_times.append(start_time)
        # end_time = row['end']
        # try:
        #     start_diff = start_time - prev_start_time
        #     invocation_periods.append(start_diff)
        #     prev_start_time = start_time
        # except:
        #     prev_start_time = start_time

        # print([start_time,end_time])
        # axs[1].plot([start_time,end_time], [start_time, start_time], c='k')

    # sorted_starts = sorted(start_times)
    # invocation_periods = [sorted_starts[i+1] - sorted_starts[i] for i in range(len(sorted_starts) - 1)]

    # print('invocation period: ' + str(1.0*sum(invocation_periods)/len(invocation_periods)))

    # try:
    #     sns.relplot(data=cgroups_df, x='timestamp', y='container_count', \
    #                 alpha=.6, marker='o', ax=axs[1])
    # except:
    #     pass

    if save_plot:
        plt.savefig(FAAS_ROOT + '/results.png')
    else:
        plt.show()

    plt.close()

    return True


def PerfMonPlotter(perf_mon_records, time_window = None):
    """
    For plotting performance monitoring records.
    """
    # Entire records
    pqos_records = perf_mon_records['pqos_records']
    # perf_records = perf_mon_records['perf_records']
    # # Select a time window if provided
    # if time_window is not None:
    #     test_start = pqos_records['timestamp'].min()
    #     time_window = [5, 10]
    #     selection_bounds = [test_start + timedelta(seconds=time_window[0]), \
    #                         test_start + timedelta(seconds=time_window[1])]
    #     pqos_records['In Test Bound'] = (pqos_records['timestamp']>selection_bounds[0]) \
    #                                     & (pqos_records['timestamp']<selection_bounds[1])
    #     perf_records['In Test Bound'] = (perf_records['timestamp']>time_window[0]) \
    #                                     & (perf_records['timestamp']<time_window[1])
    #     pqos_df = pqos_records[pqos_records['In Test Bound']==True]
    #     perf_df = perf_records[perf_records['In Test Bound']==True]

    palette = sns.color_palette("rocket_r", 16)

    # 'timestamp','Core','IPC','LLC Misses','LLC Util (KB)','MBL (MB/s)'
    fig, axs = plt.subplots(ncols=2, nrows=2, sharex=True)
    pqos_records_sum = pqos_records.groupby('timestamp').sum()
    pqos_records_sum.plot(y='IPC', ax=axs[0][0])
    pqos_records_sum.plot(y='MBL (MB/s)', ax=axs[0][1])
    pqos_records_sum.plot(y='LLC Util (KB)', ax=axs[1][0])
    pqos_records_sum.plot(y='LLC Misses', ax=axs[1][1])
    axs[0][0].set_ylim([0, 20])

    # sns.relplot(data=pqos_records, x='timestamp', y='IPC',
    #             hue='Core', kind='line', palette=palette, alpha=0.75)
    # sns.relplot(data=pqos_records, x='timestamp', y='MBL (MB/s)',
    #             hue='Core', kind='scatter', palette=palette, alpha=0.75)
    # sns.lmplot(data=pqos_df.groupby('timestamp').sum(),
    #            x='IPC', y='MBL (MB/s)', palette=palette,
    #            truncate=True, order=5, fit_reg=False,
    #            scatter_kws={'alpha':0.5}, legend_out=False)
    # sns.jointplot(data=pqos_df.groupby('timestamp').sum(),
    #               x='LLC Util (KB)', y='MBL (MB/s)', kind="hex", zorder=0)

    # cpu-cycles,L1-dcache-loads,L1-dcache-load-misses,
    # L1-icache-load-misses,dTLB-load-misses,dTLB-loads,
    # iTLB-load-misses,iTLB-loads,branch-misses,context-switches,
    # cpu-migrations,page-faults
    # sns.relplot(data=perf_records, x='timestamp', y='context-switches',
    #             kind='line', palette=palette, alpha=0.75)
    # plt.stackplot(perf_records['timestamp'], perf_records['r4f1'],
    #               perf_records['r2f1'], perf_records['r1f1'])
    # sns.relplot(data=perf_df, x='context-switches', y='r1f1',
    #             kind='scatter', palette=palette, alpha=0.75)
    # perf_records['Branch Miss Rate (%)'] = \
    #           100.0*perf_records['branch-misses']/perf_records['branches']
    # sns.lmplot(data=perf_records, x='context-switches', y='block:block_plug',
    #            truncate=True, order=8, scatter_kws={'alpha':0.5}, legend_out=False)
    # sns.jointplot(data=perf_df, x='dTLB-loads', y='iTLB-loads', kind="hex", zorder=0)

    plt.show()
    plt.close()

    return True
