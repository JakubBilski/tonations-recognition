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
LEGAL_DOTTED_DURATION_VALUES = [
    3, 6, 12, 24
]

RHYTMIC_VALUE_TO_DURATION = {
    "32" : 1,
    "16" : 2,
    "16." : 3,
    "8" : 4,
    "8." : 6,
    "4" : 8,
    "4." : 12,
    "2" : 16,
    "2." : 24,
    "1" : 32
}