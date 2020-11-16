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
    return round(sound.duration_ms/sixteenth)


def tim_to_duration(tim):
    result = []
    for num in [32, 16, 8, 4, 2, 1]:
        if tim >= num:
            result.append(16//num)
            tim -= num
    return result


def update_sounds_with_rhythmic_values_brojaczj_algorithm(tempo, beats, sounds):
    beats = list(beats)
    while beats[0] > 0:
        beats.insert(0, beats[0]-tempo)
    while beats[-1] < sounds[-1].timestamp+sounds[-1].duration_ms:
        beats.append(beats[-1]+tempo)

    dur = {}
    for s in sounds:
        id = f'{s.duration_ms:.3f}'
        dur[id] = dur.get(id, 0) + 1

    for i in range(len(sounds)):
        sounds[i].beat_id = beat_id_closest_to_timestamp(
            beats, sounds[i].timestamp)

    for s in sounds:
        duration = tim_to_duration(simple_sound_beat_dur(beats, s))
        if (len(duration) >= 3) and \
            (duration[1] == duration[0]*2) and \
                (duration[2] == duration[1]*2):
            s.rhythmic_value = str(duration[0]//2)+'.'

        elif (len(duration) >= 2) and (duration[1] == duration[0]*2):
            s.rhythmic_value = str(duration[0])+'.'
        else:
            s.rhythmic_value = str(duration[0])
