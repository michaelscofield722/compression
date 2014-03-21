#!/usr/bin/python
import sys
f = open(sys.argv[1])
for b in f.read():
  print bin(ord(b))[2:].zfill(8),
f.close()
print
