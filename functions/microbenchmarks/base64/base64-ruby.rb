# Copyright (c) 2019 Princeton University
# Copyright (c) 2014 'Konstantin Makarchev'
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

require "base64"

STR_SIZE = 1_000_000
TRIES = 100

def main(args)
  str = "a" * STR_SIZE
  str2 = ""

  s_encode = 0
  TRIES.times do |i|
    str2 = Base64.strict_encode64(str)
    s_encode += str2.bytesize
  end

  s_decode = 0
  TRIES.times do |i|
    s_decode += Base64.strict_decode64(str2).bytesize
  end

  return {'s_encode': s_encode.to_s, 's_decode': s_decode.to_s}
end
