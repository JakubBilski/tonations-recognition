SYMBOLS = ['C', 'C#', 'D', 'D#', 'E',
           'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
REVERSE_SYMBOLS = {
    s: i for i, s in enumerate(SYMBOLS)
}
REVERSE_SYMBOLS.update(
    {
        s.lower(): i for i, s in enumerate(SYMBOLS)
    }
)
REVERSE_SYMBOLS.update(
    {
        'cis': 1,
        'dis': 3,
        'fis': 6,
        'gis': 8,
        'ais': 10
    }
)
LEGAL_DURATION_VALUES = [
    1, 2, 3, 4, 6, 8, 12, 16, 24, 32
]
LEGAL_NOT_DOTTED_DURATION_VALUES = [
    1, 2, 4, 8, 16, 32
]
MIN_CHORD_DURATION = 1