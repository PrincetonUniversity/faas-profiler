/*
 Copyright (c) 2019 Princeton University

 This source code is licensed under the MIT license found in the
 LICENSE file in the root directory of this source tree.
*/

'use strict';

function main(params) {
  var currentdate = new Date();
  var timestr = "The current time is "  
                + currentdate.getHours() + ":"  
                + currentdate.getMinutes() + ":" 
                + currentdate.getSeconds();
  return { payload: timestr };
}

module.exports.main = main;
