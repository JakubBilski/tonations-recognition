import librosa

from music.sound import Sound


def get_meter(filename, sounds):
    # TODO use sounds?
    y, sr = librosa.load(filename)
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr, units='time')
    return 60/tempo, beats


def beat_id_closest_to_timestamp(beats, timestamp):
    clos = 1000
    res = -1
    for i in range(len(beats)):
        if abs(beats[i]-timestamp) < clos:
            clos = abs(beats[i]-timestamp)
            res = i

    return res


def simple_sound_beat_dur(beats, sound):
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

    # result1 = []
    # for i in range(len(result)-1):
    #     result1.append(str(result[i])+'~')
    # result1.append(result[-1])
    return result


# def symbol_to_lilypond(symbol):
#     s = symbol.lower().replace("#", "is")


def update_sounds(tempo, beats, sounds):
    beats = list(beats)
    while beats[0] > 0:
        beats.insert(0, beats[0]-tempo)
    while beats[-1] < sounds[-1].timestamp+sounds[-1].duration:
        beats.append(beats[-1]+tempo)

    dur = {}
    for s in sounds:
        id = f'{s.duration:.3f}'
        dur[id] = dur.get(id, 0) + 1

    for i in range(len(sounds)):
        sounds[i].beat_id = beat_id_closest_to_timestamp(
            beats, sounds[i].timestamp)

    sounds1 = []
    print()
    print('Sounds with beats:')
    for s in sounds:
        duration = tim_to_duration(simple_sound_beat_dur(beats, s))
        if (len(duration) >= 3) and \
            (duration[1] == duration[0]*2) and \
                (duration[2] == duration[1]*2):
            sounds1.append(Sound(
                note=s.note,
                beat_fraction=str(duration[0]//2)+'.'
            ))
        elif (len(duration) >= 2) and (duration[1] == duration[0]*2):
            sounds1.append(Sound(
                note=s.note,
                beat_fraction=str(duration[0])+'.'
            ))
        else:
            sounds1.append(Sound(
                note=s.note,
                beat_fraction=str(duration[0])
            ))

    return sounds1
