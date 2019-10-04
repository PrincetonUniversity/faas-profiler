/*
 Copyright (c) 2019 Princeton University
 
 This source code is licensed under the MIT license found in the
 LICENSE file in the root directory of this source tree.
*/

const tesseract = require('tesseractocr')

function main(params) {
    text = new Promise((resolve, reject) => {
        let text = tesseract.recognize(Buffer.from(params.__ow_body, "base64"), (err, text) => {
	    if (err) {
                var response = {
                    statusCode: 500,
                    body: "Error!"
                };
	        resolve(response);
	    } else {
                var response = {
                    statusCode: 200,
                    body: text
                };
	        resolve(response);
	    }
	});
    });
        
    return text;
}

exports.main = main;
