# Copyright (c) 2021 Princeton University, 2022 UBC
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import datetime
from os.path import exists
import unittest
from comparative_analyzer.ComparativeAnalyzer import *
import comparative_analyzer.ComparativeAnalyzer as CA 

class TestComparativeAnalyzer(unittest.TestCase):
    def test_GetTimeFromDFNameType(self):
        sample_file_name = '2021_01_18_04_37_test_data_run.pkl'
        sampleDT = GetTimeFromDFName(sample_file_name)
        self.assertTrue(isinstance(sampleDT, datetime))

    def test_GetTimeFromDFName(self):
        sample_file_name = '2021_01_18_04_37_test_data_run.pkl'
        sampleDT = GetTimeFromDFName(sample_file_name)
        self.assertEqual(str(sampleDT), '2021-01-18 04:37:00')

    @unittest.expectedFailure
    def test_GetTimeFromDFNameNoInput(self):
        sampleDT = GetTimeFromDFName(None)
        self.assertEqual(str(sampleDT), '2021-01-18 04:37:00')

    def test_ComparativeAnalyzer_Script(self):
        CA.main()
        self.assertTrue(exists("sample_comparative_plot.png"))

if __name__ == '__main__':
    unittest.main()
