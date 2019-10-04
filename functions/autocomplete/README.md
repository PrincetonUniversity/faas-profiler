# autocomplete

This is a copy of [https://github.com/ibm-watson-data-lab/serverless-autocomplete](https://github.com/ibm-watson-data-lab/serverless-autocomplete) with very minor modifications to run directly on openwhisk instead of bluemix.

This npm package is a command-line utility to help create autocomplete microservices from text files. It creates the microservice with your data embedded and returns you the URL of the service which you can use in your web forms. 

Node.js is required to install the `acsetup` utility.

## Installation

Ensure you have [Node.js and npm installed](https://nodejs.org/en/download/). Then run:

```
npm link
```

(`sudo` may also be required before this command in some cases).

## Creating autocomplete services

You can now create as many autocomplete microservices as you need. Take text file containing the strings you wish to be used. The files should contain one string per line e.g.

```
George Washington
John Adams
Thomas Jefferson
James Madison
James Monroe
```

To create an autocomplete index, simple run `acsetup` with the path to the text file of strings:

```sh
> acsetup uspresidents.txt
```

It will return you:

- the URL of your autocomplete service
- an example `curl` statement
- an HTML snippet that shows your service embedded into a web page

If you don't have data to hand then make use of the text files in the `data/` subdirectory:

```sh
acsetup countries.txt
acsetup names.txt
acsetup uktowns.txt
```

## Working with the API

Your service URL will look something like this:

    https://localhost/api/v1/web/guest/autocomplete/INDEX

where `INDEX` is the name of your index e.g. `uspresidents`.

To perform an autocomplete operation, the API call requires a `term` parameter containing the string to be completed:

    https://localhost/api/v1/web/guest/autocomplete/INDEX?term=Ge

It outputs a JSON array e.g.

```js
["George H. W. Bush","George W. Bush","George Washington","Gerald Ford"]
```

If no matches are found, an empty array is returned:

```js
[]
```

The API is compatible with the [jQuery Autocomplete API](http://api.jqueryui.com/autocomplete/) but can be plumbed into any front-end code.






