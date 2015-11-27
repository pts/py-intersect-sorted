#! /usr/bin/python
# by pts@fazekas.hu at Fri Nov 27 18:55:13 CET 2015
#
# This code works with Python 2.4, 2.5, 2.6 and 2.7. It doesn't work with
# Python 3.x.
#

import bisect
import math

def intersect_sorted_linear(a1, a2):
  s1, s2 = len(a1), len(a2)
  i1 = i2 = 0
  while i1 < s1 and i2 < s2:
    v1, v2 = a1[i1], a2[i2]
    if v1 == v2:
      yield v1
      i1 += 1
      i2 += 1
    elif v1 < v2:
      i1 += 1
    else:
      i2 += 1


assert () == tuple(intersect_sorted_linear([], ()))
assert () == tuple(intersect_sorted_linear((1, 2, 3, 4), []))
assert () == tuple(intersect_sorted_linear((), [1, 2, 3, 4]))
assert (3, 4) == tuple(intersect_sorted_linear([1,2,3,4], [3,4,5,6]))
assert (3, 3) == tuple(intersect_sorted_linear([1,2,2,3,3], [3,3,5,5,6]))


def intersect_sorted(a1, a2):
  """Yields the intersection of sorted lists a1 and a2, without deduplication.

  Execution time is O(min(lo + hi, lo * log(hi))), where lo == min(len(a1),
  len(a2)) and hi == max(len(a1), len(a2)). It can be faster depending on
  the data.
  """
  s1, s2 = len(a1), len(a2)
  i1 = i2 = 0
  if s1 and s1 + s2 > min(s1, s2) * math.log(max(s1, s2)) * 1.4426950408889634:
    bi = bisect.bisect_left
    while i1 < s1 and i2 < s2:
      v1, v2 = a1[i1], a2[i2]
      if v1 == v2:
        yield v1
        i1 += 1
        i2 += 1
      elif v1 < v2:
        i1 = bi(a1, v2, i1)
      else:
        i2 = bi(a2, v1, i2)
  else:  # The linear solution is faster.
    while i1 < s1 and i2 < s2:
      v1, v2 = a1[i1], a2[i2]
      if v1 == v2:
        yield v1
        i1 += 1
        i2 += 1
      elif v1 < v2:
        i1 += 1
      else:
        i2 += 1


assert () == tuple(intersect_sorted([], ()))
assert () == tuple(intersect_sorted((1, 2, 3, 4), []))
assert () == tuple(intersect_sorted((), [1, 2, 3, 4]))
assert (3, 4) == tuple(intersect_sorted([1,2,3,4], [3,4,5,6]))
assert (3, 3) == tuple(intersect_sorted([1,2,2,3,3], [3,3,5,5,6]))


def intersect_sorted_many(*aa):
  if aa:
    if len(aa) == 1:
      return list(aa[0])
    if len(aa) > 2:
      aa = sorted(aa, key=len)
    result = aa[0]
    is2 = intersect_sorted
    for i in xrange(1, len(aa)):
      if not result:
        break
      result = list(is2(result, aa[i]))
    return result
  else:
    return []


assert [] == intersect_sorted_many()
assert [2, 3] == intersect_sorted_many((2, 3))
assert [2] == intersect_sorted_many((2, 3), (2, 4))
assert [] == intersect_sorted_many((4, 5), (2, 3), (2, 4))
assert [2] == intersect_sorted_many((1, 2, 3), (2, 3), (2, 4))
assert [1, 3] == intersect_sorted_many((1, 2, 3), (1, 3), (1, 3, 4))


if __name__ == '__main__':
  def benchmark():
    import random
    random.seed(42)
    maxv = 3000000
    inputs = [sorted(random.randint(1, maxv) for _ in xrange(i * 200000))
              for i in xrange(1, 6)]
    import sys
    import time
    print map(len, inputs)
    t1 = time.time()
    for _ in xrange(10):
      print len(intersect_sorted_many(*inputs)),
      sys.stdout.flush()
    print
    t2 = time.time()
    # Not necessarily the same, because set does deduplication.
    for _ in xrange(10):
      print len(set.intersection(*map(set, inputs))),
      sys.stdout.flush()
    print
    t3 = time.time()
    # My benchmark results: intersect_sorted_many is about 64% (== 2.8125
    # times) faster (and uses less memory) than set.intersection.
    print [t2 - t1, t3 - t2]

  benchmark()
