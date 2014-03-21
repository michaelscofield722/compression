class CircularBuffer:

  def __init__(self, size):
    self.size = size
    self.head = -1
    self.tail = -1
    self.queue = [None]*size
  
  def add(self, data):
    for d in data:
      if self.__isFull():
        self.head = (self.head + 1) % self.size
        self.tail = (self.tail + 1) % self.size
        self.queue[self.tail] = d
      elif (self.head == -1 and self.tail == -1):
        self.head = 0
        self.tail = 0
        self.queue[self.head] = d
      elif self.tail == self.size - 1:
        self.tail = 0
        self.queue[self.tail] = d
      else:
        self.tail += 1
        self.queue[self.tail] = d

  def remove(self, size):
    while size > 0:
      if self.__isEmpty():
        return
      elif (self.head == self.tail):
        self.queue[self.head] = None
        self.head = -1
        self.tail = -1
      elif (self.head == self.size - 1):
        self.queue[self.head] == None
        self.head = 0
      else:
         self.queue[self.head] = None
         self.head = self.head + 1
      size -= 1
    return
  
  def __isFull(self):
    if (self.head == 0 and self.tail == self.size -1) or ((self.tail + 1) % self.size == self.head):
      return True
    return False
  
  def __isEmpty(self):
    if self.tail == -1 and self.head == -1:
      return True
    return False

  def get(self, index):
    i = (index + self.head) % self.size
    return self.queue[i]

  def length(self):
    if self.tail == -1 and self.head == -1:
      return 0
    if self.tail >= self.head:
      return self.tail - self.head + 1
    return (self.tail + 1) + (self.size - self.head)
  
  def debug(self):
    s = ""
    s = s + "[" + str(self.head) + ", " + str(self.tail) + "[["
    for i in range(0, self.length()):
      s = s + self.get(i)
    s = s + "]]"
    return s

  def findSubstring(self, needle):
    haystack = ''
    for i in range(0, self.length()):
      haystack = haystack + self.get(i)
    myneedle = ''
    for i in range(0, len(needle)):
      myneedle = myneedle + needle[i]
    for i in range(0, len(haystack) - len(myneedle) + 1):
      if myneedle == haystack[i : i + len(myneedle)]:
        return i, i + len(myneedle) - 1, myneedle
    return -1, -1, None

if __name__ == "__main__":
  b = CircularBuffer(4)
  print b.head, b.tail, b.queue
  b.add('ab')
  print b.head, b.tail, b.queue
  b.add('cd')
  print b.head, b.tail, b.queue
  b.add('ef')
  print b.head, b.tail, b.queue
  print b.get(0)
  print b.get(1)
  print b.get(2)
  print b.get(3)

  print b.head, b.get(b.head), b.tail, b.get(b.tail), b.queue
  b.add('ghijkl')
  print b.head, b.tail, b.queue
  b.remove(2)
  print b.head, b.tail, b.queue
  b.remove(3)
  print b.head, b.tail, b.queue
