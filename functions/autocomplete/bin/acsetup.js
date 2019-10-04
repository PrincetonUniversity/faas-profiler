#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const file = require('../lib/file.js');
const whisk = require('../lib/whisk.js');
const tmp = require('tmp');
const tmpdir = tmp.dirSync().name;

// title
console.log('openwhisk-autocomplete'.blue.bold);
if (process.argv.length < 3) {
  console.error('You must supply a filename of a file containing the strings - one per line.'.red)
  console.error('Usage: acsetup.js <filename>'.red);
  process.exit(1);
}

// load the file of strings
const filename = process.argv[2];
const arr = file.filetoarray(filename);

// get index name from the filename
const acname = file.name(filename).toLowerCase() || 'default';

// calculate paths
const datapath = path.join(tmpdir, 'data.json');
const actionpath = path.join(tmpdir, 'index.js');
const zippath = path.join(tmpdir, 'action.zip');
const sourcepath = path.join(__dirname,'..','autocomplete.js');
const templatepath = path.join(__dirname,'..','template.html');

// save the JSON array to a file
file.save(datapath, arr);

// copy the autocomplete code here
file.cp(sourcepath, actionpath);

// zip up the data and the code
file.zip(zippath, actionpath, datapath);

// send the zip file to openwhisk
console.log( ('Creating OpenWhisk action: ' + acname).green.bold )
const retval = whisk.createAction(acname, zippath);

// remove temporary files
file.rm(zippath);
file.rm(datapath);
file.rm(actionpath);

// exit on error
if (!retval) {
  process.exit(1);
}

// calculate the url of the service
const url = whisk.url(whisk.namespace(), 'autocomplete', acname);

// output the url and some sample html
var html = file.load(templatepath);
html = html.replace(/URL/g, url);
console.log();
console.log('The URL of your service is:'.blue);
console.log('  ' + url.green);
console.log();
console.log('Example curl:'.blue);
console.log(('  curl \'' + url + '?term=a\'').green);
console.log();
console.log('Example HTML:'.blue);
console.log(html.green);
