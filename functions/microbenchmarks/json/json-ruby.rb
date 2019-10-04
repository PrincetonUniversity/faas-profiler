# Copyright (c) 2019 Princeton University
# Copyright (c) 2014 'Konstantin Makarchev'
# 
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

def main(params)
    coordinates = params['coordinates']
    len = coordinates.length
    x = y = z = 0

    coordinates.each do |coord|
    x += coord['x']
    y += coord['y']
    z += coord['z']
    end

    return {'x'=> x/len, 'y'=> y/len, 'z'=> z/len}
end