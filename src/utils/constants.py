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
REVERSE_RHYTHMIC_VALUES = {
    8.0: "0",
    6.0: "1.",
    4.0: "1",
    3.0: "2.",
    2.0: "2",
    1.5: "4.",
    1.0: "4",
    0.75: "8.",
    0.5: "8",
    0.375: "16.",
    0.25: "16",
    0.1875: "32.",
    0.125: "32"
}
RHYTHMIC_VALUES = {
    REVERSE_RHYTHMIC_VALUES[key]: key for key in REVERSE_RHYTHMIC_VALUES
}
