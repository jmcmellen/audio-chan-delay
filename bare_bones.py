import wave
import sys
from struct import pack, unpack
import audioop

def chunker(seq, size):
    return (seq[pos:pos + size] for pos in xrange(0, len(seq), size))

filename = sys.argv[1]

audio = wave.open(filename, 'rb')
print audio.getnchannels()
print audio.getsampwidth()
print audio.getnframes()
print audio.getframerate()

covar_list = []

for x in xrange(65):
    for sample in chunker(audio.readframes(10000), 4):
        left = unpack("<h", sample[0:2])[0] / 8192.0 #32768.0
        right = unpack("<h", sample[2:4])[0] / 8192.0 #32768.0
        #print left, right
        covar_list.append(left * right)
    print sum(covar_list)
    covar_list = []

