# Copyright (c) 2019 Princeton University
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import matplotlib.pyplot as plt


def ComparativePlotting(t_df, p_df_dic):
        """
        Plotting result comparisons.
        """
        # possible t_df dimensions:
        # # 'start', 'duration', 'waitTime', 'initTime', 'latency'

        t_df.plot(kind='scatter', x='start', y='latency',
                  alpha=0.5, label='Total Latency', marker='o')

        # p_pqos_df = p_df_dic['pqos_records']
        # p_perf_df = p_df_dic['perf_records']
 
        plt.show()
        plt.close()
