# Copyright (c) 2021 Princeton University, 2022 UBC
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import unittest
from commons.JSONConfigHelper import ReadJSONConfig
from synthetic_workload_invoker.WorkloadChecker import *


class TestWorkloadChecker(unittest.TestCase):
    def test_supported_distributions(self):
        self.assertNotEqual(len(supported_distributions), 0)

    def test_CheckWorkloadValidity(self):
        workload = ReadJSONConfig('tests/test_data/sample_workload_configs.json')
        valid = CheckWorkloadValidity(workload)
        self.assertTrue(valid)


if __name__ == '__main__':
    unittest.main()
