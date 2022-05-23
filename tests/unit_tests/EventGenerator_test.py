# Copyright (c) 2021 Princeton University, 2022 UBC
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import unittest
from commons.JSONConfigHelper import ReadJSONConfig
from synthetic_workload_invoker.EventGenerator import *


class TestEventGenerator(unittest.TestCase):
    def test_CreateEvents_ZeroDuration(self):
        inter_arrivals = CreateEvents(instance=0, dist='Uniform',
                                      rate=1, duration=0, seed=100)
        self.assertEqual(inter_arrivals, [])

    def test_CreateEvents_ZeroRate(self):
        inter_arrivals = CreateEvents(instance=0, dist='Uniform',
                                      rate=0, duration=5, seed=100)
        self.assertEqual(inter_arrivals, [])

    def test_CreateEvents_Normal(self):
        inter_arrivals = CreateEvents(instance=0, dist='Uniform',
                                      rate=1, duration=5, seed=100)
        self.assertEqual(inter_arrivals[1:], [1.0, 1.0, 1.0, 1.0])

    def test_CreateEvents_CheckLengthUniform(self):
        inter_arrivals = CreateEvents(instance=0, dist='Uniform',
                                      rate=1000, duration=1, seed=100)
        self.assertEqual(len(inter_arrivals), 1000)

    def test_CreateEvents_CheckPoissonCoverage(self):
        inter_arrivals = CreateEvents(instance=0, dist='Poisson',
                                      rate=100, duration=5, seed=100)
        self.assertGreater(sum(inter_arrivals), 5)

    def test_EnforceActivityWindow_InvalidWindow(self):
        event_iit = EnforceActivityWindow(start_time=3.5, end_time=1.5,
                                          instance_events=[1.0, 1.0, 1.0, 1.0])
        self.assertEqual(event_iit, [])

    def test_EnforceActivityWindow_Normal(self):
        event_iit = EnforceActivityWindow(start_time=1.5, end_time=3.5,
                                          instance_events=[1.0, 1.0, 1.0, 1.0])
        self.assertEqual(event_iit, [2.0, 1.0])

    def test_GenericEventGenerator_Normal(self):
        workload = ReadJSONConfig('tests/test_data/sample_workload_configs.json')
        [all_events, event_count] = GenericEventGenerator(workload)
        self.assertEqual(sum([len(x) for x in all_events.values()]),
                         event_count)
        self.assertGreater(workload['test_duration_in_seconds'],
                           max([sum(x) for x in all_events.values()]))


if __name__ == '__main__':
    unittest.main()
