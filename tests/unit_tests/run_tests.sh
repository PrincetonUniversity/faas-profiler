# Copyright (c) 2021 Princeton University
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

GenConfigFile=../../GenConfigs.py
if [ ! -f "$GenConfigFile" ]; then
    echo "$GenConfigFile does not exist!"
    exit 1
fi

for test in $(ls ./*.py)
do
    echo $test
    python3 $test
done