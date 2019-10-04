This image resize function is a modified version of what is shown by [Nic Raboy](https://www.nicraboy.com) of [The Polyglot Developer](https://www.thepolyglotdeveloper.com) [this blog post](https://www.thepolyglotdeveloper.com/2017/12/convert-nodejs-restful-api-serverless-openwhisk/) with a fix from [here](https://github.com/oliver-moran/jimp/issues/90).

To run this, first install the npm package dependencies:

```
npm install node-zip jimp --save
```

Before we create the function, we'll need to bundle everything into a zip:

```
zip -r action.zip ./*
```

Now to create the function:

```
wsk action create img-resize --kind nodejs:8 action.zip --web raw -i
```

To get the URL that we want to curl, you'll want to run:

```
wsk action get img-resize --url -i
```

Make sure you have some PNG file in your directory. Now you can actually invoke the function! Here we invoke curl with -v for verbose.

```
curl -X POST -H "Content-Type: image/png" --data-binary @./icon.png https://localhost/api/v1/web/guest/default/img-resize -k -v >output.zip
```

Alternatively to run with the libertybell.jpg we provided:

```
curl -X POST -H "Content-Type: image/jpeg" --data-binary @./libertybell.jpg https://localhost/api/v1/web/guest/default/img-resize -k -v >output.zip
```

If it looks like you got an HTTP 200 response in the verbose output above, then output.zip should be a functioning zip archive containing the resized images.
