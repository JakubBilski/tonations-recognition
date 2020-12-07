# guitar chords levels
L1 = 0
L2 = 1
L3 = 2
L4 = 3
L5 = 4
L6 = 5

CHORDS_SCORING_MINOR = {
    0: L2,  # c
    1: L5,  # cis
    2: L2,  # d
    3: L5,  # dis
    4: L1,  # e
    5: L3,  # f
    6: L5,  # fis
    7: L2,  # g
    8: L5,  # gis
    9: L1,  # a
    10: L5,  # ais
    11: L2  # b
}

CHORDS_SCORING_MAJOR = {
    0: L2,  # c
    1: L5,  # cis
    2: L2,  # d
    3: L5,  # dis
    4: L1,  # e
    5: L3,  # f
    6: L5,  # fis
    7: L2,  # g
    8: L5,  # gis
    9: L1,  # a
    10: L5,  # ais
    11: L2  # b
}


def simplify(notes, chords, key, preview_file):
    """Transpose all piece information to a key
    in which the chords would be easier to play
    on a guitar

    Parameters:
    notes (list[Sound])
    chords (list[Chord])
    key (Key)
    preview_file (os.path-like)

    Returns:
    (list[Sound]) : Notes after transposition
    (list[Chord]) : Chords after transposition
    (Key) : Chosen easier key
    (os.path-like) : Melody with chords generated
        using transposed sounds and chords
    """
    min_score = 1000000
    min_trans = 0
    for i in range(-11, 12):
        score = 0
        for c in chords:
            if 'major' in c.kind:
                score += CHORDS_SCORING_MAJOR[(c.note + i) % 12]
            elif 'minor' in c.kind:
                score += CHORDS_SCORING_MINOR[(c.note + i) % 12]
        if score < min_score:
            min_score = score
            min_trans = i
    key.note += min_trans
    for i in range(len(notes)):
        if notes[i].note is not None:
            notes[i].note += min_trans
    for i in range(len(chords)):
        chords[i].note += min_trans
    return notes, chords, key, preview_file
