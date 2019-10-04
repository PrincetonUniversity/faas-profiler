# Copyright (c) 2019 Princeton University
# Copyright (c) 2014 'Konstantin Makarchev'
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

def main(params):
    try:
        length = len(params['coordinates'])
    except:
        return {'Error' : 'Input parameters should include coordinates.'}
    x = 0
    y = 0
    z = 0

    for coord in params['coordinates']:
        x += coord['x']
        y += coord['y']
        z += coord['z']
    
    return {'x' : x/length, 'y' : y/length, 'z' : z/length}