import music

from tonations_generation import get_tonations_from_sounds

if __name__ == "__main__":
    sounds = []
    notes = [7, 4, 4, 5, 2, 2, 0, 4, 7, 7, 4, 4, 5,
             2, 2, 0, 4, 0]  # 'a kitten climbed a fence'
    timestamp = 0.0
    duration = 0.5
    for note in notes:
        sounds.append(music.Sound(note, timestamp, duration))
        timestamp += duration
    expected_result = music.Tonation(0, None, None, 'major')
    # all transpositions
    for i in range(12):
        tonations_with_points = get_tonations_from_sounds(sounds)
        tonations_with_points.sort(key=lambda x: x.points, reverse=True)
        best_tonation = tonations_with_points[0].tonation
        print("melody: " + " ".join([str(sound.symbol) for sound in sounds]))
        if expected_result == best_tonation:
            print(f"\tSuccess! {best_tonation} = {expected_result}")
        else:
            print(f"\tFail! {best_tonation} != {expected_result}")
            print("\tBest three: ")
            for tonation_with_points in tonations_with_points[:3]:
                print(f"\t\t{tonation_with_points}")
        for sound in sounds:
            sound.note += 1
        expected_result.note += 1
