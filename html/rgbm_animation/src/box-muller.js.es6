// Box-Muller Transform (see https://en.wikipedia.org/wiki/Box–Muller_transform)

import cwise from 'cwise';
import ndarray from 'ndarray';

const compiled_normal = cwise({
  args: ['array'],
  pre: function() {
    this.shuffle = false;
  },
  body: function(a) {
    let u,
      v,
      r,
      w,
      result = 0.0;
    this.shuffle = !this.shuffle;

    if (this.shuffle) {
      do {
        u = 2.0 * Math.random() - 1.0;
        v = 2.0 * Math.random() - 1.0;
        r = u * u + v * v;
      } while (r >= 1.0);
      w = Math.sqrt((-2 * Math.log(r)) / r);
      this.next = w * v;
      result = w * u;
    } else {
      result = this.next;
    }

    a = result;
  }
});

const Normal = function(shape) {
  if (typeof shape === 'number' && shape >= 0) {
    shape = [shape];
  }
  let s = shape.reduce((acc, n) => acc * n, 1);
  var arr = new ndarray(new Float64Array(s), shape);
  compiled_normal(arr);
  return arr;
};

export default Normal;
