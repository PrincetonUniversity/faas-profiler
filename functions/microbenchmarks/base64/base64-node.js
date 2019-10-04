/*
 Copyright (c) 2019 Princeton University
 Copyright (c) 2014 'Konstantin Makarchev'

 This source code is licensed under the MIT license found in the
 LICENSE file in the root directory of this source tree.
*/

'use strict';

function main(params) {

    var STR_SIZE = 1000000;
    var TRIES = 100;

    var str = ""; for (var i = 0; i < STR_SIZE; i++) str += "a";
    var str2 = "";

    var s_encode = 0;
    for (var i = 0; i < TRIES; i++) {
        var b = new Buffer(str);
        str2 = b.toString('base64');
        s_encode += str2.length;
    }

    var s_decode = 0;
    for (var i = 0; i < TRIES; i++) {
        var b = new Buffer(str2, 'base64');
        var str3 = b.toString();
        s_decode += str3.length;
    }
  
  return { 's_encode': s_encode.toString(), 's_decode': s_decode.toString() };
}

module.exports.main = main;
