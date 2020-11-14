import music

from tonation_recognition import get_tonation

if __name__ == "__main__":
    sounds = []
    notes = [7, 4, 4, 5, 2, 2, 0, 4, 7, 7, 4, 4, 5,
             2, 2, 0, 4, 0]  # 'a kitten climbed a fence'
    timestamp = 0.0
    duration_ms = 0.5
    for note in notes:
        sounds.append(music.Sound(note, timestamp, duration_ms))
        timestamp += duration_ms
    expected_result = music.Tonation(0, None, None, 'major')
    # all transpositions
    for i in range(12):
        tonations = get_tonation(sounds)
        print("melody: " + " ".join([str(sound.symbol) for sound in sounds]))
        tonation = tonations[0]
        if expected_result == tonation:
            print(f"\tSuccess! {tonation} = {expected_result}")
        else:
            print(f"\tFail! {tonation} != {expected_result}")
        for sound in sounds:
            sound.note += 1
        expected_result.note += 1
