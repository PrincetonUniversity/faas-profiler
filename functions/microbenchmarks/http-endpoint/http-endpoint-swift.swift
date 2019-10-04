// Copyright (c) 2019 Princeton University
// Copyright (c) 2017 Serverless, Inc. http://www.serverless.com
//
// This source code is licensed under the MIT license found in the
// LICENSE file in the root directory of this source tree.

func main(args: [String:Any]) -> [String:Any] {
    let formatter = DateFormatter()
    formatter.dateFormat = "HH:mm:ss"
    let now = formatter.string(from: Date())
 
    return [ "greeting" : "The current time is \(now)" ]
}
