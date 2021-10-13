# Copyright (c) 2021 Princeton University
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

GenConfigFile=../../GenConfigs.py
if [ ! -f "$GenConfigFile" ]; then
    echo "$GenConfigFile does not exist!"
    exit 1
fi

ACTION_CREATION_TEST_STATUS=$(./action_creation.sh | tail -1)
if [[ $ACTION_CREATION_TEST_STATUS == 'FAIL' ]] 
then 
    echo 'ACTION CREATION TEST FAILED. EXITING.'
    exit
else
    echo 'ACTION CREATION TEST PASSED'
fi

ACTION_INVOCATION_TEST_STATUS=$(./action_invocation.sh | tail -1)
if [[ $ACTION_INVOCATION_TEST_STATUS == 'FAIL' ]] 
then 
    echo 'ACTION INVOCATION TEST FAILED. EXITING.'
    exit
else
    echo 'ACTION INVOCATION TEST PASSED'
fi

# More tests should be added