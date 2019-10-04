# Copyright (c) 2019 Princeton University
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

def main(args)
    time = Time.new
    return {'message' => 'The current time is ' + time.strftime("%H:%M:%S")}
end
