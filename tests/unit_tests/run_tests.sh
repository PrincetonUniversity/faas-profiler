# Copyright (c) 2021 Princeton University, 2022 UBC
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

GenConfigFile=../../GenConfigs.py
if [ ! -f "$GenConfigFile" ]; then
    echo "$GenConfigFile does not exist!"
    exit 1
fi

cd ../../
python3 -m coverage run -m unittest tests/unit_tests/*_test.py
python3 -m coverage report -m *.py
python3 -m coverage report -m commons/*.py
python3 -m coverage report -m synthetic_workload_invoker/*.py
python3 -m coverage report -m workload_analyzer/*.py
python3 -m coverage report -m comparative_analyzer/*.py
