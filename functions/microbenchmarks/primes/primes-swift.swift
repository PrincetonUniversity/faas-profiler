// Copyright (c) 2019 Princeton University
// Copyright (c) 2016 Ivan Zahariev
//
// This source code is licensed under the MIT license found in the
// LICENSE file in the root directory of this source tree.

import Foundation

func main(args: [String:Any]) -> [String:Any] {
  var n = 10_000_000

  if n < 2 {
    return [ "Number of primes found" : 0 ]
  } else if n == 2 {
    return [ "Number of primes found" : 2 ]
  }

  // do only odd numbers starting at 3
  var s = Array(stride(from: 3, to: n, by: 2))

  let mroot: Int = Int(sqrt(Double(n)))
  let half = s.count
  var i = 0
  var m = 3
  while m <= mroot {
    if s[i] != 0 {
      var j: Int = (m*m - 3) / 2
      s[j] = 0
      while j < half {
        s[j] = 0
        j += m
      }
    }
    i += 1
    m = 2*i + 3
  }
  var res = [2] + s.filter { $0 != 0 }
  return [ "Number of primes found" : res.count ]
}

