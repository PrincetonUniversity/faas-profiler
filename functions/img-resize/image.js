// This image resize function is a modified version of what is shown by [Nic Raboy](https://www.nicraboy.com) of [The Polyglot Developer](https://www.thepolyglotdeveloper.com) [this blog post](https://www.thepolyglotdeveloper.com/2017/12/convert-nodejs-restful-api-serverless-openwhisk/).
// When reproducing, you must add proper attribution within your project, documentation, etc., to the author, site, and exact links as above.
// Permission for reuse from The Polyglot Developer is strictly for the code snippets.
// Please do not copy or modify blog content such as instructive text, images, etc.

const Zip = new require('node-zip')();
const Jimp = require("jimp");

class Image {

    constructor(url) {
        this.url = url;
    }

    generate(callback) {
        return new Promise((resolve, reject) => {
            Jimp.read(this.url, (error, image) => {
                if(error) {
                    var response = {
			statusCode: 200,
                        body: "AAAAA"
                    };
                    resolve(response);
                }
                var images = [];
                images.push(image.resize(196, 196).getBufferAsync(Jimp.AUTO).then(result => {
                    return new Promise((resolve, reject) => {
                        resolve({
                            size: "xxxhdpi",
                            data: result
                        });
                    });
                }));
                images.push(image.resize(144, 144).getBufferAsync(Jimp.AUTO).then(result => {
                    return new Promise((resolve, reject) => {
                        resolve({
                            size: "xxhdpi",
                            data: result
                        });
                    });
                }));
                images.push(image.resize(96, 96).getBufferAsync(Jimp.AUTO).then(result => {
                    return new Promise((resolve, reject) => {
                        resolve({
                            size: "xhdpi",
                            data: result
                        });
                    });
                }));
                images.push(image.resize(72, 72).getBufferAsync(Jimp.AUTO).then(result => {
                    return new Promise((resolve, reject) => {
                        resolve({
                            size: "hdpi",
                            data: result
                        });
                    });
                }));
                images.push(image.resize(48, 48).getBufferAsync(Jimp.AUTO).then(result => {
                    return new Promise((resolve, reject) => {
                        resolve({
                            size: "mdpi",
                            data: result
                        });
                    });
                }));
                Promise.all(images).then(data => {
                    for(var i = 0; i < data.length; i++) {
                        Zip.file(data[i].size + "/icon.png", data[i].data);
                    }
                    var d = Zip.generate({ base64: true, compression: "DEFLATE" });
                    var response = {
                        headers: {
                            "Content-Type": "application/zip",
                            "Content-Disposition": "attachment; filename=android.zip"
                        },
                        body: d
                    };
                    resolve(response);
                });
            });
        });
    }

}

module.exports = Image;
