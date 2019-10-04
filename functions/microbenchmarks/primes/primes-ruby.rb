# Copyright (c) 2019 Princeton University
# Copyright (c) 2016 Ivan Zahariev
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.


def main(params)
  n = 10000000
  
  return {'Number of primes found' => 0} if n  < 2
  return {'Number of primes found' => 2} if n == 2

  # do only odd numbers starting at 3
  s = 3.upto(n + 1).select(&:odd?)

  mroot = n ** 0.5
  half = s.length
  i = 0
  m = 3
  until m > mroot do
    if s[i]
      j = (m * m - 3) / 2
      s[j] = nil
      until j >= half do
        s[j] = nil
        j += m
      end
    end
    i += 1
    m = 2 * i + 3
  end

  res = [2] + s.compact
  return {'Number of primes found' => res.length}
end
