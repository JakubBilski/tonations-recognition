from os import times
from time import time
import librosa
from librosa import beat


def get_meter(filename, sounds):
    # TODO use sounds?
    y, sr = librosa.load(filename)
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr, units='time')
    return tempo, beats


def simple_sound_dur1(tempo, beats, duration):
    return round(float(duration)*8/tempo)/8


def simple_sound_dur2(tempo, beats, duration):
    desired = [
        0.125,
        0.25,
        0.5,
        0.75,
        1,
        1.5,
        2,
        2.5,
        3
    ]
    closest = 1000
    result = -1
    for d in desired:
        if abs(duration/tempo-d) < closest:
            closest = abs(duration/tempo)
            result = d

    return result


def update_sounds(tempo, beats, sounds):
    # TODO update length of sounds to fit meter
    # round(sound.duration*8/meter)/8  <- it is an idea

    print("Time diffs:")
    for i in range(len(sounds)-1):
        print(
            f"\t{sounds[i+1].duration/sounds[i].duration:.3f}\t{sounds[i].symbol}\t{sounds[i].duration:.3f}")

    dur = {}
    for s in sounds:
        id = f'{s.duration:.3f}'
        dur[id] = dur.get(id, 0) + 1

    print('Sound duration:')
    for key in sorted(dur):
        s_d = simple_sound_dur2(tempo, beats, float(key))
        print(f"\t{key}: {dur[key]}\t{s_d}")

    return sounds


def beat_id_closest_to_timestamp(beats, timestamp):
    clos = 1000
    res = -1
    for i in range(len(beats)):
        if abs(beats[i]-timestamp) < clos:
            clos = abs(beats[i]-timestamp)
            res = i

    return res


def simple_sound_beat_dur3(beats, sound):
    id = sound.beat_id
    b1 = beats[id]
    b2 = beats[id+1]
    sixteenth = (b2-b1)/4
    return round(sound.duration/sixteenth)
    # if abs(sound.timestamp-b1) < 0.05:
    #     # super


def tim_to_duration(tim):
    result = []
    for num in [32, 16, 8, 4, 2, 1]:
        if tim >= num:
            result.append(16//num)
            tim -= num

    result1 = []
    for i in range(len(result)-1):
        result1.append(str(result[i])+'~')
    result1.append(result[-1])
    return result1
    


# def symbol_to_lilypond(symbol):
#     s = symbol.lower().replace("#", "is")



def update_sounds1(tempo, beats, sounds):
    # TODO update length of sounds to fit meter
    # round(sound.duration*8/meter)/8  <- it is an idea

    print(f"Tempo: {tempo}\t{60/tempo:.3f}")
    app_beat = 60/tempo

    beats = list(beats)
    while beats[0] > 0:
        beats.insert(0, beats[0]-app_beat)
    while beats[-1] < sounds[-1].timestamp+sounds[-1].duration:
        beats.append(beats[-1]+app_beat)

    dur = {}
    for s in sounds:
        id = f'{s.duration:.3f}'
        dur[id] = dur.get(id, 0) + 1

    print('Sound duration:')
    for key in sorted(dur):
        s_d = simple_sound_dur2(tempo, beats, float(key))
        print(f"\t{key}: {dur[key]}\t{s_d}")

    for i in range(len(sounds)):
        sounds[i].beat_id = beat_id_closest_to_timestamp(
            beats, sounds[i].timestamp)

    print()
    print('Sounds with beats:')
    for s in sounds:
        print(
            f"\t{s.timestamp:.3f} {s.symbol.ljust(5)}\t{s.duration:.3f} {beats[s.beat_id]:.3f} {beats[s.beat_id+1]:.3f}\t{beats[s.beat_id+1]-beats[s.beat_id]:.3f}")

    print()
    print('Sounds with beats:')
    for s in sounds:
        print(f"\t{s.timestamp:.3f} {s.symbol.ljust(5)}\t{s.duration:.3f} {simple_sound_beat_dur3(beats, s)}")

    
    with open("result.ly", 'w') as f:
        print('\\version "2.12.3"', file=f)
        print('\\relative c\' {', file=f)
        print('\\time 4/4', file=f)
        for s in sounds:
            tim = simple_sound_beat_dur3(beats, s)
            durations = tim_to_duration(tim)
            for dur in durations:
                if s.note is None:
                    if '~' in str(dur):
                        dur = dur[:-1]
                    f.write(f" r{dur}")
                else:
                    f.write(f" {s.symbol.lower().replace('#', 'is')}{dur}")
        print('', file=f)
        # print('\\midi', file=f)
        print('}', file=f)

    return sounds
