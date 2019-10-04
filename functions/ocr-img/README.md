This function makes use of the open source [tesseract OCR engine](https://github.com/tesseract-ocr/tesseract) and a javascript wrapper for it called [tesseractocr](https://www.npmjs.com/package/tesseractocr).

To create the function, we will make use of a docker image that contains both [nodejs from openwhisk](https://github.com/apache/incubator-openwhisk-runtime-nodejs) and tesseractocr:

```
wsk action create ocr-img handler.js --docker immortalfaas/nodejs-tesseract --web raw -i
```

To get the URL that we want to curl, you'll want to run:

```
wsk action get ocr-img --url -i
```

Make sure you have some PNG file in your directory. Now you can actually invoke the function! Here we invoke curl with -v for verbose.

```
curl -X POST -H "Content-Type: image/png" --data-binary @./img.png https://localhost/api/v1/web/guest/default/ocr-img -k -v >output.txt
```

To run with a jpeg instead, try pitontable.jpg with the following command:

```
curl -X POST -H "Content-Type: image/jpeg" --data-binary @./pitontable.jpg https://localhost/api/v1/web/guest/default/ocr-img -k -v >output.txt
```

If it looks like you got an HTTP 200 response in the verbose output above, then output.txt will contain the OCR output from your image.
