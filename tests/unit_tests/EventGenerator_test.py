# Copyright (c) 2021 Princeton University
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import sys
import unittest
sys.path.insert(1, '../..')
from synthetic_workload_invoker.EventGenerator import *

class TestEventGenerator(unittest.TestCase):
    def test_CreateEvents(self):
        inter_arrivals = CreateEvents(instance=0, dist='Uniform', rate=1, duration=5, seed=100)
        self.assertEqual(inter_arrivals[1:], [1.0, 1.0, 1.0, 1.0])
    
    def test_EnforceActivityWindow(self):
        event_iit = EnforceActivityWindow(start_time=1.5, end_time=3.5, 
                                          instance_events=[1.0, 1.0, 1.0, 1.0])
        self.assertEqual(event_iit, [2.0, 1.0])

if __name__ == '__main__':
    unittest.main()