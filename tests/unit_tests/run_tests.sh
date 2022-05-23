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
cp tests/test_data/2021_01_18_04_37_test_data_run.pkl data_archive
python3 -m coverage run -m unittest tests/unit_tests/*_test.py
python3 -m coverage report -m *.py
python3 -m coverage report -m commons/*.py
python3 -m coverage report -m synthetic_workload_invoker/*.py
python3 -m coverage report -m workload_analyzer/*.py
python3 -m coverage report -m comparative_analyzer/*.py
rm data_archive/2021_01_18_04_37_test_data_run.pkl
rm sample_comparative_plot.png
