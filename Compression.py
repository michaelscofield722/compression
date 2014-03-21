from Buffer import CircularBuffer
from FileStream import OutputFileStream
from FileStream import InputFileStream
from BinaryWriter import BinaryWriter
from BinaryReader import BinaryReader
import pickle

class LZ77:

  def __init__(self, lasize = 16, lusize = 4096):
    self.lasize = lasize
    self.lusize = lusize
    self.lookahead = []*self.lasize
    self.lookup = CircularBuffer(self.lusize)
    self.buf = CircularBuffer(self.lusize)
    self.maxlen = lasize
    self.filesystemblock = 4096

  def compress(self, filename):
    try:
      inp = open(filename, 'rb')
    except:
      print "File does not exist!"
      exit()

    bw = BinaryWriter(filename+".lz", self.filesystemblock)
    prevMatched = None 
    prevStart = -1
    prevEnd = -1
    while True:
      byte = inp.read(1)
      if byte == '':
        break
      self.lookahead.append(byte)
      start, end, match = self.lookup.findSubstring(self.lookahead)
      if match == None and prevMatched == None: 
          bw.appendBit(0)
          bw.appendByte(ord(byte))
          self.lookahead = []
          self.lookup.add(byte)
      else:
        if match == None and prevMatched != None:
          if len(prevMatched) > 1:
            length = len(prevMatched)
            distance = self.lookup.length() - prevStart - 1
            bw.appendBit(1)
            bw.append3Nibble(distance)
            bw.appendNibble(length)
            self.lookahead = []
          else:
            bw.appendBit(0)
            bw.appendByte(ord(prevMatched))
            self.lookahead = []
          self.lookahead.append(byte)
          self.lookup.add(prevMatched)
          prevMatched = None
          start, end, match = self.lookup.findSubstring(self.lookahead)
          if match == None:
            bw.appendBit(0)
            bw.appendByte(ord(byte))
            self.lookahead = []
            self.lookup.add(byte)
          else:
            prevMatched = match
            prevStart = start
            prevEnd = end
            continue
        elif len(match) == self.lasize:
          length = len(match)
          distance = self.lookup.length() - start - 1
          bw.appendBit(1)
          bw.append3Nibble(distance)
          bw.appendNibble(length)
          self.lookahead = []
          prevMatched = None
          self.lookup.add(match)
        else:
          prevMatched = match
          prevStart = start
          prevEnd = end
    if prevMatched != None and len(prevMatched) > 0:
      length = len(prevMatched)
      distance = self.lookup.length() - start - 1
      bw.appendBit(1)
      bw.append3Nibble(distance)
      bw.appendNibble(length)
    elif prevMatched != None:
      bw.appendBit(0)
      bw.appendByte(ord(prevMatched))
    elif match != None:
      bw.appendBit(0)  
      bw.appendByte(ord(match))
    bw.close()
    inp.close()

  def decompress(self, filename):
    self.lookup = CircularBuffer(self.lusize)
    br = BinaryReader(filename, self.filesystemblock)
    bw = BinaryWriter(filename+".decomp", self.filesystemblock)
    while True:
      bit = br.readBit()
      if bit == None:
        break
      if bit == 0:
        sym = br.readByte()
        if sym == None:
          break
        print "SYM: ", chr(sym)
        bw.appendByte(sym)
        self.lookup.add(chr(sym))
      else:
        distance = br.read3Nibble()
        length = br.readNibble()
        print distance
        print length
        if distance == None or length == None:
          break
        index = self.lookup.length() - distance - 1
        for i in range(0, length):
          sym = self.lookup.get(index)
          index = index + 1
          print "SYM: ", sym
          bw.appendByte(ord(sym))
          self.lookup.add(sym)
    br.close()
    bw.close()     

  def debug(self, res):
    self.sprint("LOOKAHEAD", self.lookahead, len(self.lookahead))
    self.sprint("RES", res)
    self.sprint("LOOKUP", self.lookup.queue)
    self.sprint()

  def sprint(self, *args):
    '''for a in args:
      print a,
    print'''
    return
