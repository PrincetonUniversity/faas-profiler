// Copyright (c) 2019 Princeton University
//
// This source code is licensed under the MIT license found in the
// LICENSE file in the root directory of this source tree.

import Foundation

func main(args: [String:Any]) -> [String:Any] {
    let strsize = 1_000_000
    let tries = 100
    let longString = String(repeating: "a", count: strsize)
    let data = longString.data(using: .utf8)
    var base64en:Data? = nil
    var s_encode: Int = 0

    //Encode
    for _ in 0..<tries {
        base64en = data!.base64EncodedData()
        s_encode = s_encode &+ base64en!.endIndex
    }

    //Dencode
    var s_decode: Int = 0
    for _ in 0..<tries {
        s_decode = s_decode &+ Data(base64Encoded: base64en!)!.endIndex
    }

    return [ "s_encode" : String(s_encode), "s_decode" : String(s_decode) ]
}
