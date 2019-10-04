const assert = require('assert');
const ac = require('../autocomplete.js');
ac.setPath('./test/data.json');

const decodeResponse = function(obj) {
  obj.body = JSON.parse(Buffer.from(obj.body, 'base64').toString());
};

describe('autocompelete tests', function() {

  it('should return object', function() {
    var r = ac.main({term: 'mi'});
    assert(typeof r === 'object');
    assert(typeof r.statusCode === 'number');
    assert(typeof r.headers === 'object');
    assert(typeof r.body === 'string');
  });

  it('should return a 200', function() {
    var r = ac.main({term: 'mi'});
    assert(typeof r === 'object');
    assert.equal(r.statusCode, 200);
  });

  it('should have correct content-type', function() {
    var r = ac.main({term: 'mi'});
    assert(typeof r.headers === 'object');
    assert.equal(r.headers['Content-Type'], 'application/json');
  });

  it('should autocomplete from the start of the file', function() {
    var r = ac.main({term: 'a'});
    decodeResponse(r);
    assert.deepEqual(r.body, ["Aaren","Aarika","Abagael","Abagail","Abbe","Abbey","Abbi","Abbie","Abby","Abbye","Abigael","Abigail","Abigale","Abra","Ada","Adah","Adaline","Adan","Adara","Adda"]);
  });

  it('should autocomplete to the end of the file', function() {
    var r = ac.main({term: 'zuz'});
    decodeResponse(r);
    assert.deepEqual(r.body, ["Zuzana"]);
  });

  it('should autocomplete in the middle of the file file', function() {
    var r = ac.main({term: 'step'});
    decodeResponse(r);
    assert.deepEqual(r.body, ["Stepha","Stephana","Stephani","Stephanie","Stephannie","Stephenie","Stephi","Stephie","Stephine"]);
  });

  it('should return empty array for no matches', function() {
    var r = ac.main({term: 'asfasfasfa'});
    decodeResponse(r);
    assert.deepEqual(r.body, []);
    assert.equal(r.body.length, 0);
  });

  it('should cope with spaces', function() {
    var r = ac.main({term: 'zsa z'});
    decodeResponse(r);
    assert.deepEqual(r.body, ['Zsa Zsa']);
  });

  it('should cope with missing term', function() {
    var r = ac.main({});
    decodeResponse(r);
    assert.deepEqual(r.body, []);
  });

  it('maximum of twenty return values', function() {
    var r = ac.main({ term: 'b'});
    decodeResponse(r);
    assert(r.body.length <= 20);
  });

  it('should be case insensitive', function() {
    var r = ac.main({ term: 'Bil'});
    decodeResponse(r);
    assert.deepEqual(r.body, ["Bili","Bill","Billi","Billie","Billy","Billye"]);
  });

  it('should ignore odd chars', function() {
    var r = ac.main({ term: ' Bil*!%'});
    decodeResponse(r);
    assert.deepEqual(r.body, ["Bili","Bill","Billi","Billie","Billy","Billye"]);
  });

});