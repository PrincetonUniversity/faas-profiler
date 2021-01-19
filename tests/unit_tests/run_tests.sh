# Copyright (c) 2021 Princeton University
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

for test in $(ls ./*.py)
do
    echo $test
    python3 $test
done