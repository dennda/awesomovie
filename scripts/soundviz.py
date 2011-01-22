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

    def samples(self):
        lineno = 0
        for line in self.fd:
            lineno += 1
            if line.startswith('#'):
                continue
            elements = line.strip().split(" ")
            # [0] cause we discard the imaginary part, almost identical to
            # actual magnitude.
            sample = [eval(element)[0] for element in elements]
            num_bins = len(sample)
            if num_bins != self.freq_bins:
                _sample = []
                val = 0.
                i = 0
                bin_width = num_bins / self.freq_bins
                for freq in sample:
                    if i == bin_width:
                        _sample.append(val)
                        val = 0.
                        i = 0
                    val += freq
                    i += 1
                sample = _sample
            assert len(sample) == self.freq_bins

            self._samples.append(sample)
            yield sample
        self.fd.close()
        #raise StopIteration


from time import time, sleep
channel1s = Song('kanal1s_trans3', freq_bins=20)
last = time()
# SPS = samples / tracklength
sps = 1371. / 127.
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

