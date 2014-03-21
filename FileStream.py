from Buffer import CircularBuffer

class OutputFileStream:
  def __init__(self, fp, size = 1024):
    self.fp = fp
    self.size = size
    self.data = bytearray()
  
  def writesym(self, sym):
    if len(self.data) > self.size-1:
      self.fp.write(self.data)
      self.__flush()
    self.data.append(0)
    self.data.append(sym)

  def writepattern(self, distance, length):
    if len(self.data) > self.size-2:
      self.fp.write(self.data)
      self.__flush()
    self.data.append(1)
    self.data.append(distance)
    self.data.append(length)
  
  def write(self, chars):
    for c in chars:
      if len(self.data) > self.size:
        self.fp.write(self.data)
        self.__flush()
      self.data.append(c)

  def __flush(self):
    self.data = bytearray()
  
  def close(self):
    self.fp.write(self.data)
    self.__flush()
    self.fp.close()

class InputFileStream:
  def __init__(self, fp, size = 4096):
    self.fp = fp
    self.size = size
    self.data = CircularBuffer(size)
  
  def readdata(self):
    indicator = self.__readsym()
    if indicator == '':
      return ''
    if ord(indicator) == 0:
      sym = self.__readsym()
      self.data.add(sym)
      return sym
    else:
      syms = []
      distance = ord(self.__readsym())
      length = ord(self.__readsym())
      bufferlen = self.data.length()
      start = bufferlen - distance - 1
      while length > 0:
        syms.append(self.data.get(start))
        start += 1
        length -= 1
      sym = "".join(syms)
      self.data.add(sym)
      return sym

  def __readsym(self):
    return self.fp.read(1)
  
  def close(self):
    self.data.remove(self.data.length())
    self.fp.close()
