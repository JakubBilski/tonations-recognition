POINTS = {
    "major": [
        1,
        0,
        0.3,
        0,
        1,
        0,
        0,
        1,
        0,
        0,
        0.3,
        0.1
    ],
    "minor": [
        1,
        0,
        0.3,
        1,
        0,
        0,
        0,
        1,
        0,
        0,
        0.3,
        0
    ],
    "diminished": [
        1,
        0,
        0,
        1,
        0,
        0,
        1,
        0,
        0,
        0,
        0,
        0
    ]
}
POINTS["major7"] = POINTS["major"]

COEFS = {
    "major": 1,
    "major7": 1,
    "minor": 0.99,
    "diminished": 0.5
}

# additional coef for first sound matching
FIRST_SOUND = 1.1

# next chord dict:
# NEXT_CHORD[previous chord level][next chord level] = coefficient
NEXT_CHORD = {
    0: {  # 0 means start of the song
        # first chord is always tonic
        1: 1000
    },
    5: {
        # tonic or 6-th level after dominant
        1: 1.2,
        6: 1.2,
        # never subdominant
        2: 0,
        4: 0
    },
}
# prefer not changing chords
for i in range(1, 8):
    if i not in NEXT_CHORD:
        NEXT_CHORD[i] = {}
    NEXT_CHORD[i][i] = 1.2
