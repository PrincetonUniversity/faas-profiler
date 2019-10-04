const fs = require('fs');
const path = require('path');
const child_process = require('child_process');
var spawn = child_process.spawnSync;

const filterStr = function(str) {
  return str.toLowerCase().replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g,"").trim();
};

const load = function(filename) {
  return fs.readFileSync(filename, { encoding: 'utf8'});
};

const filetoarray = function(filename) {
  // read the input file
  const content = load(filename);

  // split into lines
  // trim whitespace
  // remove blank ines
  // turn into the form: simplfied*original
  // e.g. great ayton north yorks*Great Ayton (North Yorks)
  return content
    .split('\n')
    .map(function(v) { return v.trim(); })
    .filter(function(v){ return v;})
    .map(function(v) { return filterStr(v) + '*' + v; })
    .sort();
};

const cp = function(src, dest) {
  if (!fs.existsSync(src)) {
    return false;
  }
  const data = fs.readFileSync(src, 'utf-8');
  fs.writeFileSync(dest, data);
  return true;
};

const save = function(filename, data) {
  fs.writeFileSync(filename, JSON.stringify(data), { encoding: 'utf8'});
};

const rm = function(path) {
  fs.unlinkSync(path);
};

const zip = function(zipfilename, file1, file2) {
  // spawn a child process (synchronous)
  spawn('zip', ['-j', zipfilename, file1, file2]);
};

const name = function(filename) {
  const parsed = path.parse(filename);
  return parsed.name;
}

module.exports = {
  filetoarray: filetoarray,
  cp: cp,
  rm: rm,
  load: load,
  save: save,
  zip: zip,
  name: name
}
