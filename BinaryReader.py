#!/usr/bin/python
import os

class BinaryReader(object):
  def __init__(self, fpath, max_size = 4096):
    self.fp = open(fpath, "rb")
    self.max_size = max_size
    self.buff = bytearray(max_size)
    self.bitlen = 0
    self.currentbit = 0
    self.filesize = os.path.getsize(fpath)

  def populateBuffer(self):
    self.bitlen = self.fp.readinto(self.buff) * 8
    self.currentbit = 0

  def readBit(self):
    if self.currentbit == self.filesize*8:
      return None
    if self.currentbit == self.bitlen:
      self.populateBuffer()
    byteIndex = self.currentbit / 8
    bitIndex = 7 - self.currentbit % 8
    tmp = self.buff[byteIndex]
    tmp = tmp & (1 << bitIndex)
    self.currentbit = self.currentbit + 1
    if tmp == 0:
      return 0
    return 1

  def readByte(self):
    bits = 8
    bit = 0
    tmp = 0
    while bits > 0:
      bit = self.readBit()
      if bit == None:
        break
      tmp = (tmp << 1) | bit
      bits -= 1
    if bit == None and bits > 0:
      return None
    '''tmp = (tmp << 1) | self.readBit()
    tmp = (tmp << 1) | self.readBit()
    #print "Nibble1", bin(tmp)[2:]
    tmp = (tmp << 1) | self.readBit()
    tmp = (tmp << 1) | self.readBit()
    tmp = (tmp << 1) | self.readBit()
    tmp = (tmp << 1) | self.readBit()
    #print "Nibble2", bin(tmp)[2:]'''
    return tmp


  def readNibble(self):
    bits = 4
    bit = 0
    tmp = 0
    while bits > 0:
      bit = self.readBit()
      if bit == None:
        break
      tmp = (tmp << 1) | bit
      bits -= 1
    if bit == None and bits > 0:
      return None
    return tmp
    '''tmp = self.readBit()
    tmp = (tmp << 1) | self.readBit()
    tmp = (tmp << 1) | self.readBit()
    tmp = (tmp << 1) | self.readBit()
    return tmp
	'''

  def read3Nibble(self):
    bits = 12
    bit = 0
    tmp = 0
    while bits > 0:
      bit = self.readBit()
      if bit == None:
        break
      tmp = (tmp << 1) | bit
      bits -= 1
    if bit == None and bits > 0:
      return None
    return tmp
    '''tmp = self.readNibble()
    tmp = (tmp << 4) | self.readNibble()
    tmp = (tmp << 4) | self.readNibble()
    return tmp'''

  def close(self):
    self.fp.close()

if __name__ == "__main__":
  br = BinaryReader("/tmp/akhi.txt", 2)
  print bin(br.readBit())[2:],
  print bin(br.readBit())[2:],
  print bin(br.readBit())[2:],
  print bin(br.readBit())[2:],
  print bin(br.readBit())[2:],
  print bin(br.readBit())[2:],
  print bin(br.readBit())[2:],
  print bin(br.readBit())[2:],
  print bin(br.readBit())[2:],
  print bin(br.readBit())[2:],
  print bin(br.readBit())[2:],
  print bin(br.readByte())[2:]
  print bin(br.readByte())[2:],
  print bin(br.readNibble())[2:],
  print bin(br.readNibble())[2:],
  print bin(br.read3Nibble())[2:],
