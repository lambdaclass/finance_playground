// Box-Muller Transform (see https://en.wikipedia.org/wiki/Box–Muller_transform)

const cwise = require("cwise");
const ndarray = require("ndarray");

const compiled_normal = cwise({
  args: ["array"],
  pre: function() {
    this.shuffle = false;
  },
  body: function(a) {
    var u,
      v,
      r = 0.0;
    this.shuffle = !this.shuffle;

    if (this.shuffle) {
      do {
        u = 2.0 * Math.random() - 1.0;
        v = 2.0 * Math.random() - 1.0;
        r = u * u + v * v;
      } while (r >= 1.0);
      var w = Math.sqrt((-2 * Math.log(r)) / r);
      this.next = w * v;
      a = w * u;
    } else {
      a = this.next;
    }
  }
});

const Normal = function(shape) {
  if (typeof shape === "number" && shape >= 0) {
    shape = [shape];
  }
  var s = shape.reduce((acc, n) => acc * n, 1);
  var arr = new ndarray(new Float64Array(s), shape);
  compiled_normal(arr);
  return arr;
};

module.exports = Normal;
