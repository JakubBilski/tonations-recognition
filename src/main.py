import tonation


symbols = ['C', 'C#', 'D', 'D#', 'E',
           'F', 'F#', 'G', 'G#', 'A', 'A#', 'H']


if __name__ == "__main__":
    t = tonation.Tonation(symbols.index("C"), 0, 100, "dur")
    print(t)
