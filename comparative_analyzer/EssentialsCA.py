# Copyright (c) 2019 Princeton University
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

# Includes a bunch of common functions which can be used by different
# functions in the Comparative Analyzer module.

import copy
import pandas as pd


def GetFuncInvocationDF(meta_df):
    """
    Returns a DF containing test name, list of functions, and
    corresponding list of invocation rates.
    Input: meta_df (a.k.a., combined_stat_df)
    """
    tmp_test_funclist_df = meta_df.groupby(meta_df['test'])['func_name'].apply(list).to_frame()
    tmp_test_ratelist_df = meta_df.groupby(meta_df['test'])['rate'].apply(list).to_frame()
    return pd.merge(tmp_test_funclist_df, tmp_test_ratelist_df, on='test')


def MergeDictionaries(dic1, dic2):
    """
    merging dic2 into dic1 (both dictionaries)
    """
    l_dic1 = copy.copy(dic1)
    for key in dic2.keys():
        try:
            if key in l_dic1.keys():
                l_dic1[key].append(dic2[key])
            else:
                l_dic1[key] = [dic2[key]]
        except:     # empty dic1
            l_dic1 = {key: [dic2[key]]}
    return l_dic1


def MergeTwoListsAsDic(keys, values):
    """
    """
    dic = {}
    for i in range(len(keys)):
        dic[keys[i]] = values[i]

    return dic
