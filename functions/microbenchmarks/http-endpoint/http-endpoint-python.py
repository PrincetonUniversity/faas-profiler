# Copyright (c) 2019 Princeton University
# Copyright (c) 2017 Serverless, Inc. http://www.serverless.com
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import json
import datetime

def main(params):
    current_time = datetime.datetime.now().time()
    body = {
        "message": "The current time is " + str(current_time)
    }
    return body
