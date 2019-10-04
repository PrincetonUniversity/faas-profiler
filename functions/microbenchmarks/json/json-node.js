/*
Copyright (c) 2019 Princeton University
Copyright (c) 2014 'Konstantin Makarchev'

This source code is licensed under the MIT license found in the
LICENSE file in the root directory of this source tree.
*/

'use strict';

function main(params) {
    var coordinates = params["coordinates"];
    var len = coordinates.length;
    var x = 0;
    var y = 0;
    var z = 0;
    var coord = 0;

    for (var i = 0; i < coordinates.length; i++) {
        coord = coordinates[i];
        x += coord["x"];
        y += coord["y"];
        z += coord["z"];
    }

    return { "x": x/len, "y": y/len, "z": z/len};
}