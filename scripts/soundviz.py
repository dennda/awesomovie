

class Song(object):
    def __init__(self, filename, freq_bins=4096):
        self.fn = filename
        self.fd = open(self.fn, 'rb')
        self._samples = []
        self.freq_bins = freq_bins

    def samples(self):
        lineno = 0
        for line in self.fd:
            lineno += 1
            if line.startswith('#'):
                continue
            elements = line.strip().split(" ")
            # [0] cause we discard the imaginary part, almost identical to
            # actual magnitude.
            sample = [abs(int(float(element))) for element in elements]
            num_bins = len(sample)
            #if num_bins != self.freq_bins:
            #    _sample = []
            #    val = 0.
            #    i = 0
            #    bin_width = num_bins / self.freq_bins
            #    print bin_width
            #    for freq in sample:
            #        if i == bin_width:
            #            _sample.append(val)
            #            val = 0.
            #            i = 0
            #        val += freq
            #        i += 1
            #    sample = _sample
            #print len(sample), self.freq_bins
            #assert len(sample) == self.freq_bins

            self._samples.append(sample)
            yield sample
        self.fd.close()
        #raise StopIteration


channel1s = Song('left.dat', freq_bins=20)


from bpy.ops.anim import *

scene = bpy.context.scene
scene.frame_end = 3048

assert frames == samples

num_freqs = len(samples[0])
for freqno in range(num_freqs):
    spacing = 10
    location = (freqno * spacing, 0, 0)
    bpy.ops.mesh.primitive_cube_add(location=location)

for frameno in range(frames):
    change_frame(frame=frameno)

    # Set all object properties

    # Set scaling keying set
    bpy.ops.anim.keyframe_insert_menu(type=-3)


#from math import log
#from time import time, sleep
#last = time()
## SPS = samples / tracklength
#sps = 24.
#time_per_sample = 127. / 3059. #(1. / sps) * (1. / 3059.)
#drop = False
#for sample in channel1s.samples():
#    now = time()
#    if drop:
#        last = now
#        drop = False
#        continue
#    # Quickly clear the terminal:
#    print '\x1b[H\x1b[J'
#    for index, freq in enumerate(sample):
#        #print freq
#        if index > 20:
#            break
#        print "." * (freq / 2)
#    diff = now - last
#    wait = time_per_sample - diff
#    if diff < time_per_sample:
#        sleep(abs(wait))
#    else:
#        drop = True
#    last = now

