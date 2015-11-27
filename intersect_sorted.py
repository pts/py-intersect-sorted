# This code works in Python >=2.4 and 3.x.

def intersect_sorted(a1, a2):
  """Yields the intersection of sorted lists a1 and a2, without deduplication.

  Execution time is O(min(lo + hi, lo * log(hi))), where lo == min(len(a1),
  len(a2)) and hi == max(len(a1), len(a2)). It can be faster depending on
  the data.
  """
  import bisect, math
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
