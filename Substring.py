from Buffer import CircularBuffer

def findSubstring(haystack, needle):
  return hackedFindSubstr(haystack, needle)

def hackedFindSubstr(haystack, needle):
    myhaystack = ''
    for i in range(0, haystack.length()):
        myhaystack = myhaystack + haystack.get(i)
    myneedle = ''
    for i in range(0, needle.length()):
        myneedle = myneedle + needle.get(i)
    # print "MyHaystack:", myhaystack
    # print "MyNeedle:", myneedle
    while myneedle != '':
      for i in range(0, len(myhaystack) - len(myneedle) + 1):
        # print "Compare:",myhaystack[i : i + len(myneedle)], myneedle
        if myneedle == myhaystack[i : i + len(myneedle)]:
          return i, i + len(myneedle) - 1, myneedle
      myneedle = myneedle[:-1]
    return -1, -1, ''

def properFindSubStr(haystack, needle):
    needle.debug()
    m = [[0] * (1 + needle.length()) for i in xrange(1 + haystack.length())]
    longest, x_longest = 0, 0
    for x in xrange(1, 1 + haystack.length()):
        for y in xrange(1, 1 + needle.length()):
            if haystack.get(x - 1) == needle.get(y - 1):
                m[x][y] = m[x - 1][y - 1] + 1
                if m[x][y] > longest:
                    longest = m[x][y]
                    x_longest = x
            else:
                m[x][y] = 0
    result = ''
    for i in range(x_longest-longest, x_longest):
        data = haystack.get(i) 
        if data != None:
            result += data
    return x_longest-longest, x_longest, result

if __name__ == "__main__":
  haystack = CircularBuffer(10)
  haystack.add("abcdeabcde")
  haystack.remove(2)
  haystack.add("a")
  print "Len: ",haystack.length(), haystack.queue, haystack.head, haystack.tail
  needle = CircularBuffer(5)
  needle.add("bcde")
  print "Result =", findSubstring(haystack, needle)


