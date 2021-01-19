# Copyright (c) 2021 Princeton University
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

# This script reads the WSK_PATH from the GenConfigs.py in the root directory.
# Make sure that it is correctly set before running this test.  
WSK_PATH=$(grep -r "WSK_PATH" ../../GenConfigs.py | cut -d' ' -f 3)
WSK_PATH=${WSK_PATH:1:-1}

echo '### ACTION CREATION TEST ###'

TEST_STATUS='PASS'

# copy all base64 functions here
cp ../../functions/microbenchmarks/base64/base64-* .

# create functions
$WSK_PATH action create base64-nodejs base64-node.js -i
$WSK_PATH action create base64-python base64-python.py -i
$WSK_PATH action create base64-ruby base64-ruby.rb -i
$WSK_PATH action create base64-swift base64-swift.swift -i

# check that those actions are created
if $WSK_PATH action list -i | grep 'base64-nodejs';
then echo '>> base64-nodejs successfully created';
else echo '>> base64-nodejs not created'; TEST_STATUS='FAIL';
fi
if $WSK_PATH action list -i | grep 'base64-python';
then echo '>> base64-python successfully created'; 
else echo '>> base64-python not created'; TEST_STATUS='FAIL';  
fi
if $WSK_PATH action list -i | grep 'base64-ruby';
then echo '>> base64-ruby successfully created'; 
else echo '>> base64-ruby not created'; TEST_STATUS='FAIL';  
fi
if $WSK_PATH action list -i | grep 'base64-swift';
then echo '>> base64-swift successfully created'; 
else echo '>> base64-swift not created'; TEST_STATUS='FAIL';  
fi

echo $TEST_STATUS