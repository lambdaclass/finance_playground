/* Utilities from NumJS (https://github.com/nicolaspanel/numjs/) */

const cwise = require('cwise');

function initNativeArray(shape, i) {
  i = i || 0;
  var c = shape[i] | 0;
  if (c <= 0) {
    return [];
  }
  var result = new Array(c);
  var j;
  if (i === shape.length - 1) {
    for (j = 0; j < c; ++j) {
      result[j] = 0;
    }
  } else {
    for (j = 0; j < c; ++j) {
      result[j] = initNativeArray(shape, i + 1);
    }
  }
  return result;
}

var doUnpack = cwise({
  args: ['array', 'scalar', 'index'],
  body: function unpackCwise(arr, a, idx) {
    var v = a;
    var i;
    for (i = 0; i < idx.length - 1; ++i) {
      v = v[idx[i]];
    }
    v[idx[idx.length - 1]] = arr;
  }
});

function unpackArray(arr) {
  var result = initNativeArray(arr.shape, 0);
  doUnpack(arr, result);
  return result;
}

function range(n) {
  return Array.apply(null, Array(n)).map(function(_, i) {
    return i;
  });
}

module.exports = { unpackArray: unpackArray, range: range };
