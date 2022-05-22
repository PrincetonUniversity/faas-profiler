# Copyright (c) 2021 Princeton University, 2022 UBC
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import unittest
from workload_analyzer.WorkloadAnalyzer import GetTestMetadata


class TestWorkloadAnalyzer(unittest.TestCase):
    def test_GetTestMetadata(self):
        test_start_time, config_file = \
         GetTestMetadata(test_metadata_file='tests/test_data/test_metadata.out')
        self.assertEqual([test_start_time, config_file],
                         [1610944442298, 'test_data_run_config.json'])


if __name__ == '__main__':
    unittest.main()
