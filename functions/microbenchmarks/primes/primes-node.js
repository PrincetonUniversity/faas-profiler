/* 
 Copyright (c) 2019 Princeton University
 Copyright (c) 2016 Ivan Zahariev

 This source code is licensed under the MIT license found in the
 LICENSE file in the root directory of this source tree.
*/

'use strict';

function main(main) {
    var n = 10000000;

	if (n < 2) { return {"Number of primes found": 0}; }
	if (n == 2) { return {"Number of primes found": 2}; }

	var s = [];
	for (var i = 3; i < n + 1; i += 2) {
		s.push(i);
	}

	var mroot = Math.floor(Math.sqrt(n));
	var half = s.length;
	var i = 0;
	var m = 3;

	while (m <= mroot) {
		if (s[i]) {
			var j = Math.floor((m*m-3)/2);   // int div
			s[j] = 0;
			while (j < half) {
				s[j] = 0;
				j += m;
			}
		}
		i = i + 1;
		m = 2*i + 3;
	}

	// due to a bug in node.js 4.3, we need to declare and init on separate lines
	// or else node.js performs about four times slower
	var res = [];
	res.push(2);

	for (var x = 0; x < s.length; x++) {
		if (s[x]) {
			res.push(s[x]);
		}
	}
	return {"Number of primes found": res.length};
}
