import audiogen
import sys
import itertools

with open("aa.wav", 'w') as f:
    audiogen.sampler.write_wav(
        f,
        itertools.cycle(itertools.chain(audiogen.beep(), audiogen.silence(0.5)))
    )