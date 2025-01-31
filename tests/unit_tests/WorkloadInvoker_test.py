# Copyright (c) 2023 UBC
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import unittest
from synthetic_workload_invoker.WorkloadInvoker import *


class TestWorkloadInvoker(unittest.TestCase):
    def test_HTTPInstanceGeneratorGenerics(self):
        status = HTTPInstanceGeneratorGeneric(
            IATs=[1.0, 1.0, 1.0, 1.0],
            blocking_cli=0,
            url="http://127.0.0.1:8080",
            data="",
        )
        self.assertTrue(status)

    def test_HTTPInstanceGeneratorGenerics_with_empty_instance_times(self):
        status = HTTPInstanceGeneratorGeneric(
            IATs=[],
            blocking_cli=0,
            url="http://127.0.0.1:8080",
            data="",
        )
        self.assertFalse(status)

    def test_HTTPInstanceGeneratorGenerics_with_empty_url(self):
        status = HTTPInstanceGeneratorGeneric(
            IATs=[1.0, 1.0, 1.0, 1.0],
            blocking_cli=0,
            url="",
            data="",
        )
        self.assertFalse(status)

    def test_HTTPInstanceGeneratorGenerics_with_invalid_url(self):
        status = HTTPInstanceGeneratorGeneric(
            IATs=[1.0, 1.0, 1.0, 1.0],
            blocking_cli=0,
            url="www.http.s",
            data="",
        )
        self.assertFalse(status)


if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(unittest.TestLoader().loadTestsFromTestCase(TestWorkloadInvoker))
