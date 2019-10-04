const child_process = require('child_process');
const spawn = child_process.spawnSync;
const colors = require('colors');

// get the openwhisk namespace
const namespace = function() {
  // get the names space that wsk is publishing to
  var ns = spawn( 'wsk', ['namespace', 'list', '-i']);
  var str = ns.stdout.toString('utf8');
  var bits = str.split('\n');
  var retval = null;
  if (bits.length >= 2 && bits[0] === 'namespaces') {
    retval = bits[1];
  }
  return retval.trim();
};

// deploy an action
const createAction = function(name, path) {

  // create package
  var packageParams = ['package', 'update', 'autocomplete', '-i'];
  var packageCreate = spawn( 'wsk', packageParams);

  if(packageCreate.status) {
    // package could not be created/updated; display error and abort processing
    console.error(packageCreate.stderr.toString('utf8').red);
    return false;
  }

  // create OpenWhisk action
  // I5: apply workaround for server-side issue
  var createParams = ['action', 'update', 'autocomplete/'+name, '--kind', 'nodejs:6', path, '-a', 'web-export', 'true', '-i'];
  var actionCreate = spawn( 'wsk', createParams);

  if(actionCreate.status) {
    // action could not be created/updated; display error and abort processing
    console.error(actionCreate.stderr.toString('utf8').red);
    return false;
  }

  return true;
};

const url = function(namespace, package, action) {
  return 'https://localhost/api/v1/web/' + namespace + '/' + package + '/' + action;
}


module.exports = {
  namespace: namespace,
  createAction: createAction,
  url: url
};
