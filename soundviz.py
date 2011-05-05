#from bpy.ops.anim import *
#
#scene = bpy.context.scene
#scene.frame_end = 3048
#change_frame(frame=0)


class Song(object):
    def __init__(self, filename, freq_bins=4096):
        self.fn = filename
        self.fd = open(self.fn, 'rb')
        self._samples = []
        self.freq_bins = freq_bins

    def getFrame(self, frame):
        if(len(self._samples) <frame):
            self.skipTo(frame)
        return self._samples[frame-1]
    
    def skipTo(self, frame):
        self.size()

    def samples(self):
        lineno = 0
        for line in self.fd:
            if line.startswith('#'):
                continue
            lineno += 1
            elements = line.strip().split(" ")
            sample = [eval(element) for element in elements]
            if(lineno-1 == len(self._samples)):
                self._samples.append(sample)
            yield sample
        #self.fd.close()
        self.fd.seek(0)
        #raise StopIteration

    def size(self):
        self.fd.seek(0)
        lineno = 0
        num_bins = self.freq_bins
        for line in self.fd:
            if line.startswith('#'):
                continue
            lineno += 1
            # [0] cause we discard the imaginary part, almost identical to
            # actual magnitude.
            elements = line.strip().split(" ")
            if(lineno-1 == len(self._samples)):
                sample = [eval(element) for element in elements]
                num_bins_this = len(sample)
                self._samples.append(sample)
                if(lineno >1 and num_bins_this != num_bins):
                    print("WARNING: not all line have the same amount of columns")
                else:
                    num_bins=num_bins_this
        self.fd.seek(0)
        return (lineno, num_bins)
     
     
"""
from time import time, sleep
channel1s = Song('left.dat', freq_bins=20)
last = time()
# SPS = samples / tracklength
sps = 24.
time_per_sample = 1. / sps

drop = False
for sample in channel1s.samples():
    now = time()
    if drop:
        last = now
        drop = False
        continue
    # Quickly clear the terminal:
    print '\x1b[H\x1b[J'
    for freq in sample:
        #print freq
        ampl = max(0, int(freq))
        print "." * ampl
    diff = now - last
    wait = time_per_sample - diff
    if diff < time_per_sample:
        sleep(abs(wait - 0.005))
    else:
        drop = True
    last = now
"""
