# Copyright (c) 2021 Princeton University
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import sys
import unittest
sys.path.insert(1, '../..')
from commons.JSONConfigHelper import ReadJSONConfig
from synthetic_workload_invoker.WorkloadChecker import *
from synthetic_workload_invoker.WorkloadInvoker import *

class TestWorkloadChecker(unittest.TestCase):
    def test_supported_distributions(self):
        self.assertNotEqual(len(supported_distributions), 0)

    def test_CheckWorkloadValidity(self):
        workload = ReadJSONConfig('../test_data/sample_workload_configs.json')
        valid = CheckWorkloadValidity(workload, supported_distributions)
        self.assertTrue(valid)

if __name__ == '__main__':
    unittest.main()