import sounds_generation
import chords_generation
import music


if __name__ == "__main__":
    pitch = [1, 2, 3, 4, 5, 6, 6.5, 7, 9,
             10, 11, 12, 13, 14, 15, 15.5, 16, 18]
    notes = [7, 4, 4, 5, 2, 2, 0, 4, 7, 7, 4, 4, 5, 2, 2, 0, 4, 0]
    s = sounds_generation.get_sounds_from_list(pitch, notes)
    print(f"song: {s}")
    chords = chords_generation.get_chords(
        s, music.Tonation(0, 0, 0, "major"), 3, 1)
    print(f"chords: {chords}")
