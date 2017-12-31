'''
Expression Tone Generator
'''
from math import pi, sin
from os import system

import numpy as np
from scipy.io.wavfile import write


class ETG:
    rate, secs, mode = 44100, 15, 'stereo'  # default wave values

    def __init__(self, rate=rate, secs=secs, mode=mode):
        self.set(rate, secs, mode)

    def funcL(self, t):  # virtuals w/ (L,R) channel funcs, L=MONO
        pass

    def funcR(self, t):
        pass

    def set(self, rate, secs, mode):
        self.rate, self.secs, self.mode = rate, secs, mode

    def generate(self):
        def scale(input, min=-1, max=1):
            'scale min..max'
            input -= np.min(input)
            input /= np.max(input) / (max - min)
            input += min
            return input

        ' return numpy array evaluating func in a float32 -1..+1 range'
        if self.mode == 'mono':  # generate (size,) w/ funcL
            w = np.asarray([self.funcL(wp) for wp in np.arange(0, self.secs, 2. * pi / self.rate)], dtype=np.float32)
        elif self.mode == 'stereo':  # generate (size,2) array
            w = np.asarray(
                [[func(wp) for func in (self.funcL, self.funcR)] for wp in
                 np.arange(0, self.secs, 2. * pi / self.rate)],
                dtype=np.float32)
        else:
            w = []  # error

        return scale(w)

    def osPlayer(self):  # return os play command
        import platform
        os_player = {'Darwin': 'afplay', 'Linux': 'aplay', 'Windows': 'start'}
        return os_player[platform.system()]


class ETGbw(ETG):
    'derive from ETG and implement virtuals (funcL, funcR)'

    # 2 channel (L,R) functions 440hz tone + 2hz brainwave + 2hz amp oscilator
    def funcL(self, t):
        return sin(2 * t) * sin(440 * t)

    def funcR(self, t):
        return sin(2.2 * t) * sin(442 * t)


if __name__ == '__main__':
    etgStereo = ETGbw(rate=41000, secs=20, mode='stereo')
    write('etgStereo.wav', rate=etgStereo.rate, data=etgStereo.generate())
    etgMono = ETGbw(rate=41000, secs=20, mode='mono')
    write('etgMono.wav', rate=etgMono.rate, data=etgMono.generate())

    system(ETG().osPlayer() + ' etgMono.wav')
    system(ETG().osPlayer() + ' etgStereo.wav')
