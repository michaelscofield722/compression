import sys
import time 
from Compression import LZ77

start = time.time()
la = 4
lu = 8
if len(sys.argv) > 2:
  la = int(sys.argv[2])
if len(sys.argv) > 3:
  lu = int(sys.argv[3])
#c = LZ77(la, lu)
c = LZ77()
c.compress(sys.argv[1])
intermediate = time.time()
print intermediate - start
c.decompress(sys.argv[1]+'.lz')
print time.time() - intermediate

