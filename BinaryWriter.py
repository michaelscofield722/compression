#!/usr/bin/python

class BinaryWriter(object):
  def __init__(self, fpath, max_size = 4096):
    self.fp = open(fpath, "wb")
    self.max_size = max_size
    self.buff = bytearray(max_size)
    self.bitlen = 0

  def writeSymbol(self, byteVal):
	self.appendBit(0)
	self.appendByte(byteVal)
	print "Sym: %c" % (byteVal)

  def writeDistLen(self, d, l):
	self.appendBit(1)
	self.append3Nibble(d)
	self.appendNibble(l)
	print "DL : %d %d" % (d, l)

  def appendBit(self, bitVal):
    #print "Appending bit", bitVal
    byteIndex = self.bitlen / 8
    bitIndex = 7 - self.bitlen % 8
    if (bitVal == 1):
      self.buff[byteIndex] = self.buff[byteIndex] | (1 << bitIndex)
      self.bitlen = self.bitlen + 1
    else:
      tmp = 1 << bitIndex
      tmp = ~tmp
      tmp = 0xFF & tmp
      self.buff[byteIndex] = self.buff[byteIndex] & tmp
      self.bitlen = self.bitlen + 1
    self.flush()
    #self.debugStr()

  def appendByte(self, byteVal):
    #print "Appending byte", byteVal, bin(byteVal)[2:]
    # Fittable MSBs
    remainingBits = 8 - (self.bitlen % 8)
    #print "RB",remainingBits
    tmp = byteVal
    tmp = tmp >> (8 - remainingBits)
    byteIndex = self.bitlen / 8
    #self.buff[byteIndex] = self.buff[byteIndex] & (0xFF << (8 - remainingBits))
    self.buff[byteIndex] = self.buff[byteIndex] & 0xFF
    #print "BUFF: ", bin(self.buff[byteIndex])[2:].zfill(8)
    self.buff[byteIndex] = self.buff[byteIndex] | tmp
    #print "BUFF: ", bin(self.buff[byteIndex])[2:].zfill(8)
    self.bitlen = self.bitlen + remainingBits
    self.flush()
    #self.debugStr()
    # Remaining LSBs
    remainingBits = 8 - remainingBits
    #print "RB",remainingBits
    if remainingBits == 0:
      return
    tmp = byteVal
    tmp = tmp << (8 - remainingBits)
    tmp = tmp & 0xFF
    tmp = tmp & (0xFF << (8 - remainingBits))
    byteIndex = self.bitlen / 8
    self.buff[byteIndex] = self.buff[byteIndex] | tmp
    #print bin(self.buff[byteIndex])
    self.bitlen = self.bitlen + remainingBits
    self.flush()
    #self.debugStr()
  '''
    tmp = 128
    for i in range(0,8):
      if (tmp & byteVal) > 0:
        self.appendBit(1)
      else:
        self.appendBit(0)
      tmp = tmp / 2
  '''

  def appendNibble(self, fourbits):
    #print "Appending fourbits", fourbits, bin(fourbits)[2:]
    tmp = 8
    for i in range(0,4):
      if (tmp & fourbits) > 0:
        self.appendBit(1)
      else:
        self.appendBit(0)
      tmp = tmp / 2

  def append3Nibble(self, twelvebits):
    #print "3 Nibbles", twelvebits, bin(twelvebits)[2:]
    self.appendNibble((twelvebits & 0xF00) >> 8)
    self.appendNibble((twelvebits & 0xF0) >> 4)
    self.appendNibble(twelvebits & 0xF)

  def flush(self, force = True):
    if self.bitlen == self.max_size * 8:
      print "Flushing...."
      #for i in range(len(self.buff)):
      #  print bin(self.buff[i])[2:],
      self.fp.write(self.buff)
      self.bitlen = 0
      self.buff = bytearray(self.max_size)

  def close(self):
    num_bytes = (self.bitlen + 7 ) / 8
    self.fp.write(self.buff[0 : num_bytes])
    #for i in range(num_bytes):
    #  print bin(self.buff[i])[2:],
    self.fp.flush()
    self.fp.close()

  def debugStr(self):
    print "[" + str(self.bitlen) + "]",
    for i in range(0, (self.bitlen + 7) / 8):
      print bin(self.buff[i])[2:].zfill(8),
    print


if __name__ == "__main__":
  bw = BinaryWriter("/tmp/akhi.txt", 2)
  bw.appendBit(1)
  bw.appendBit(1)
  bw.appendBit(0)
  bw.appendBit(1)
  bw.appendBit(1)
  bw.appendBit(1)
  bw.appendBit(0)
  bw.appendBit(1)
  bw.appendBit(1)
  bw.appendBit(0)
  bw.appendBit(1)
  bw.appendByte(0xC9)
  bw.appendByte(0xC9)
  bw.appendNibble(0xA)
  bw.appendNibble(0x5)
  bw.append3Nibble(0xABC)
  bw.close()

